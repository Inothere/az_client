import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base
from conf import DATABASES


world_engine: sa.engine.base.Engine = sa.create_engine(
    DATABASES["world"]["uri"], echo=DATABASES["world"]["echo"]
)
WorldBase = declarative_base()
