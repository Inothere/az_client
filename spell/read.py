import typing
from dbc import CustomDBCFile
from dbcpy.records.spell_record import SpellRecord
from dbc.records import SpellMechanicRecord, SpellRadiusRecord, SpellRangeRecord
import csv

from sqlalchemy_utils.listeners import force_auto_coercion


class BaseReader:
    record_type = None

    def __init__(self, filename: str) -> None:
        self.filename = filename

    def to_csv(self, output: str):
        with open(self.filename, "rb") as f:
            data = []
            dbc = CustomDBCFile.from_file(f, self.record_type)
            for record in dbc.records:
                data.append(self.form_csv_row(record))
        if not data:
            return
        headers = list(data[0].keys())
        with open(output, "w") as f:
            writer = csv.DictWriter(f, headers, dialect=csv.unix_dialect)
            writer.writeheader()
            writer.writerows(data)

    def form_csv_row(self, record: typing.Any) -> typing.Dict:
        raise NotImplementedError()


class SpellReader(BaseReader):
    record_type = SpellRecord

    def form_csv_row(self, record: typing.Any) -> typing.Dict:
        return {
            "id": record.entry,
            "name": record.name.de_de,
            "subname": record.subname.de_de,
            "description": record.description.de_de,
            "tooltip": record.tooltip.de_de,
            "stack_amount": record.stack_amount,
            "range": record.range,
            "cooldown": record.cooldown,
            "global_cooldown": record.global_cooldown,
            "effect": record.effect,
            "effect1": record.effect1,
            "effect2": record.effect2,
            "effect_radius": record.effect_radius,
            "effect_radius1": record.effect_radius1,
            "effect_radius2": record.effect_radius2,
            "effect_apply_aura_name": record.effect_apply_aura_name,
            "effect_apply_aura_name1": record.effect_apply_aura_name1,
            "effect_apply_aura_name2": record.effect_apply_aura_name2,
            "effect_base_points": record.effect_base_points,
            "effect_base_points1": record.effect_base_points1,
            "effect_base_points2": record.effect_base_points2,
            "spell_level": record.spell_level,
            "mana_cost": record.mana_cost,
        }


class SpellRadiusReader(BaseReader):
    record_type = SpellRadiusRecord

    def form_csv_row(self, record: typing.Any) -> typing.Dict:
        return {
            "id": record.id,
            "radius": record.radius,
            "radius_per_level": record.radius_per_level,
            "radius_max": record.radius_max,
        }


class SpellMechanicReader(BaseReader):
    record_type = SpellMechanicRecord

    def form_csv_row(self, record: typing.Any) -> typing.Dict:
        return {"id": record.id, "state_name": record.state_name.de_de}


class SpellRangeReader(BaseReader):
    record_type = SpellRangeRecord

    def form_csv_row(self, record: typing.Any) -> typing.Dict:
        return {
            "id": record.id,
            "min_range_hostile": record.min_range_hostile,
            "min_range_friend": record.min_range_friend,
            "max_range_hostile": record.max_range_hostile,
            "max_range_friend": record.max_range_friend,
            "flags": record.flags,
            "display_name": record.display_name.de_de,
            "display_name_short": record.display_name_short.de_de,
        }


if __name__ == "__main__":
    reader = SpellReader(r"/Users/chendi/Downloads/dbc/spell.dbc")
    reader.to_csv("spell.csv")
