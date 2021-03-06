import typing
from dbcpy.dbc_file import DBCFile
from dbcpy.records.spell_record import SpellRecord
import csv


class BaseReader:
    record_type = None

    def __init__(self, filename: str) -> None:
        self.filename = filename

    def to_csv(self, output: str):
        with open(self.filename, "rb") as f:
            data = []
            dbc = DBCFile.from_file(f, self.record_type)
            for record in dbc.records:
                data.append(self.form_csv_row(record))
        if not data:
            return
        headers = list(data[0].keys())
        with open(output, "w") as f:
            writer = csv.DictWriter(f, headers, dialect=csv.excel_tab)
            writer.writeheader()
            writer.writerows(data)

    def form_csv_row(record: typing.Any) -> typing.Dict:
        raise NotImplementedError()


class SpellReader(BaseReader):
    record_type = SpellRecord

    def form_csv_row(record: typing.Any) -> typing.Dict:
        return {
            "id": record.entry,
            "name": record.name.en_us,
            "subname": record.subname.en_us,
            "cooldown": record.cooldown,
            "global_cooldown": record.global_cooldown,
            "spell_level": record.spell_level,
            "mana_cost": record.mana_cost,
        }
