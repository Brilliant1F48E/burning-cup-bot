from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()

from .db_interaction import DBInteraction
