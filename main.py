from npc.creator import VendorCreator
from base import world_engine
import sqlalchemy as sa


with world_engine.connect() as conn:
    creator = VendorCreator(conn)
    creator.do_create(
        "warrior super vendor", ["Willey's Portable Howitzer", "Primed Musket"]
    )
