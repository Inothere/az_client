from sqlalchemy.orm.attributes import flag_modified
from dbcpy.loc import Loc
import dataclasses


_test_fields = {"id": int, "name": Loc}


TestRecord = dataclasses.make_dataclass(
    "TestRecord", zip(_test_fields.keys(), _test_fields.values())
)
TestRecord.field_types = staticmethod(_test_fields.values())


_spell_radius_fields = {
    "id": int,
    "radius": float,
    "radius_per_level": float,
    "radius_max": float,
}

SpellRadiusRecord = dataclasses.make_dataclass(
    "SpellRadiusRecord", zip(_spell_radius_fields.keys(), _spell_radius_fields.values())
)
SpellRadiusRecord.field_types = staticmethod(_spell_radius_fields.values())


_spell_mech_fields = {
    "id": int,
    "state_name": Loc
}

SpellMechanicRecord = dataclasses.make_dataclass(
    "SpellMechanicRecord", zip(_spell_mech_fields.keys(), _spell_mech_fields.values())
)
SpellMechanicRecord.field_types = staticmethod(_spell_mech_fields.values())

_spell_range_fields = {
    "id": int,
    "min_range_hostile": float,
    "min_range_friend": float,
    "max_range_hostile": float,
    "max_range_friend": float,
    "flags": int,
    "display_name": Loc,
    "display_name_short": Loc
}

SpellRangeRecord = dataclasses.make_dataclass(
    "SpellRangeRecord", zip(_spell_range_fields.keys(), _spell_range_fields.values())
)
SpellRangeRecord.field_types = staticmethod(_spell_range_fields.values())