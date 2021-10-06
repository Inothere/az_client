from npc.creator import VendorCreator
from base import world_engine
from npc.bis import BIS
from dbc.dbc import CustomDBCFile, Loc
from dbc.records import TestRecord
from dbcpy.records.spell_record import SpellRecord
from spell.read import SpellReader, SpellRadiusReader, SpellMechanicReader, SpellRangeReader


creator = VendorCreator(world_engine.connect())
creator.do_create(
    "猎人60级BIS",
    BIS["猎人"]
)
