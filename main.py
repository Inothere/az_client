from npc.creator import VendorCreator
from base import world_engine
from npc.bis import BIS


with world_engine.connect() as conn:
    creator = VendorCreator(conn)
    creator.do_create(
        "战士装备供应商",
        BIS["战士"]
    )
