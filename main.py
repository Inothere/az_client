from npc.creator import VendorCreator
from base import world_engine
from npc.bis import BIS
from dbc.dbc import CustomDBCFile, Loc
from dbc.records import TestRecord
from dbcpy.records.spell_record import SpellRecord
from spell.read import SpellReader

reader = SpellReader("/Users/chendi/Downloads/dbc/spell.dbc") 
reader.to_csv('spell.csv')
