from npc.creator import VendorCreator
from base import world_engine
from npc.bis import BIS
from dbc.dbc import CustomDBCFile, Loc
from dbc.records import TestRecord
import io


f = io.BytesIO()
dbc_file: CustomDBCFile = CustomDBCFile.new(f, TestRecord)
record = TestRecord(
    id=1,
    name=Loc(    
        en_us='测试',
        en_gb='伙计',
        ko_kr='3',
        fr_fr='4',
        de_de='5',
        en_cn='6',
        zh_cn='7',
        en_tw='8',
        zh_tw='9',
        es_es='10',
        es_mx='11',
        ru_ru='12',
        pt_pt='13',
        pt_br='14',
        it_it='15',
        unknown='16',
        flag=0
    )
)
dbc_file.records.append(record)

with open('test.dbc', 'wb') as out:
    dbc_file.write_to_file(lambda x: x, out)

with open('test.dbc', 'rb') as out:
    dbc_file: CustomDBCFile = CustomDBCFile.from_file(out, TestRecord)
    for record in dbc_file.records:
        print(record.id, record.name.en_us)
