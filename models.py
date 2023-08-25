from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

Base = declarative_base()

class ItemType(Base):
    __tablename__ = 'item_types'
    id = Column(Integer, primary_key=True)
    type = Column(String, unique=True)
    keywords = relationship("Keyword", back_populates="item_type")

class Keyword(Base):
    __tablename__ = 'keywords'
    id = Column(Integer, primary_key=True)
    keyword = Column(String)
    item_type_id = Column(Integer, ForeignKey('item_types.id'))
    item_type = relationship("ItemType", back_populates="keywords")

def initialize_db(engine):
    Base.metadata.create_all(engine)
    
def populate_initial_data(session):
    cat = ItemType(type='cat')
    dog = ItemType(type='dog')
    pet = ItemType(type='pet')
    cat.keywords = [Keyword(keyword='some_keyword')]
    dog.keywords = [Keyword(keyword='some_keyword')]
    pet.keywords = [Keyword(keyword='some_keyword')]
    
    session.add(cat)
    session.add(dog)
    session.add(pet)
    session.commit()
