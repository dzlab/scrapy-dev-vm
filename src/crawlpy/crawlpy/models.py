__author__ = 'dzlab'
# source: http://newcoder.io/scrape/part-3/

from sqlalchemy import create_engine, Column, Integer, String, DateTime, Text, Numeric
from sqlalchemy.engine.url import URL
from sqlalchemy.ext.declarative import declarative_base

import settings

DeclarativeBase = declarative_base()

def db_connect():
    """
    Performs database connection using database settings from settings.py.
    Returns sqlalchemy engine instance
    """
    return create_engine(URL(**settings.DATABASE))

def create_rentals_table(engine):
    """"""
    DeclarativeBase.metadata.create_all(engine)


class RentalAds(DeclarativeBase):
    """Sqlalchemy rental ads model"""
    __tablename__ = "rentals"

    id = Column(Integer, primary_key=True)
    reference = Column('reference', String)
    title = Column('title', String)
    description = Column('description', String)
    link = Column('link', String, nullable=True)
    location = Column('location', String, nullable=True)
    price = Column('price', Numeric, nullable=True)
    fees = Column('fees', Numeric, nullable=True)
    surface = Column('surface', String)
    floor = Column('floor', String)
    room = Column('room', String)
    constructedIn = Column('constructedIn', Integer)