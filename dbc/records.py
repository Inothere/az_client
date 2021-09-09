from dbcpy.loc import Loc
import dataclasses


_test_fields = {
    "id": int,
    "name": Loc
}


TestRecord = dataclasses.make_dataclass('TestRecord', zip(_test_fields.keys(), _test_fields.values()))
TestRecord.field_types = staticmethod(_test_fields.values())