from dbcpy.dbc_file import DBCFile, DBCHeader, RecordIterator, RecordReader
import dbcpy.loc as loc
import dbcpy.bytes_util as bytes_util
from dbcpy.loc import Loc


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
    @classmethod
    def from_file(cls, f, record_type):
        header = DBCHeader.from_file_handle(f)
        f.seek(header.size + header.record_size * header.record_count)
        string_block = f.read()
        records = RecordIterator(f, header, CustomRecordReader(record_type), string_block)
        return cls(header, records)
