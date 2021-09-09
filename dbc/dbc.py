from dbcpy.dbc_file import DBCFile, DBCHeader, RecordIterator, RecordReader
import dbcpy.bytes_util as bytes_util
from dbcpy.loc import Loc
import itertools


def custom_read_dbc_string(offset, strings):
    b_list = []
    while strings[offset] != 0:
        b_list.append(strings[offset].to_bytes(length=1, byteorder='big'))
        offset += 1
    codes = b''.join(b_list)
    return codes.decode()


class CustomRecordReader(RecordReader):
    def read_record(self, strings, f):
        int32_size = 4
        float_size = 4
        record_fields = []
        for field_type in self._record_type.field_types:
            if field_type is int:
                record_fields.append(bytes_util.to_int(f.read(int32_size)))
            if field_type is float:
                record_fields.append(bytes_util.to_float(f.read(float_size)))
            elif field_type is Loc:
                raw_loc = [bytes_util.to_int(f.read(int32_size)) for _ in range(17)]
                strs = (custom_read_dbc_string(offset, strings) for offset in raw_loc[0:16])
                record_fields.append(Loc(*strs, raw_loc[16]))
        return self._record_type(*record_fields)


class CustomDBCFile(DBCFile):
    def write_to_file(self, transform, f):
        string_block_offset = self.header.size + self.header.record_count * self.header.record_size
        f.seek(string_block_offset)
        f.write(b'\0')
        string_block_size = 1

        # reserve the first 20 bytes for the header
        f.seek(self.header.size)

        for record in map(transform, self.records):
            for field in record.__dict__.values():
                if isinstance(field, Loc):
                    for string in itertools.islice(field.__dict__.values(), 16):
                        if string:
                            f.write(bytes_util.to_bytes(string_block_size))
                            pos = f.tell()
                            f.seek(string_block_offset + string_block_size)
                            encoded = (string + '\0').encode('utf-8')
                            f.write(encoded)
                            # 源码中是按照编码前的长度递进，导致非ascii编码offset计算错误
                            # string_block_size 必须按照utf8编码后的字节码长度递进
                            string_block_size += len(encoded)
                            f.seek(pos)
                        else:
                            f.write(bytes_util.to_bytes(0))
                    f.write(bytes_util.to_bytes(field.flag))
                else:
                    f.write(bytes_util.to_bytes(field))

        f.seek(0)
        self.header.string_block_size = string_block_size
        f.write(self.header.to_bytes())

    @classmethod
    def from_file(cls, f, record_type):
        header = DBCHeader.from_file_handle(f)
        f.seek(header.size + header.record_size * header.record_count)
        string_block = f.read()
        records = RecordIterator(f, header, CustomRecordReader(record_type), string_block)
        return cls(header, records)

    @classmethod
    def new(cls, f, record_type):
        record_size = 0
        field_count = 0
        for field_type in record_type.field_types:
            if field_type is int or field_type is float:
                record_size += 4
            else:
                record_size += 4 * 17
            field_count += 1
        header = DBCHeader(
            magic=b'WDBC',
            record_count=0,
            field_count=field_count,
            record_size=record_size,
            string_block_size=0,
            size=20
        )
        return cls(header, RecordIterator(f, header, CustomRecordReader(record_type), b''))
