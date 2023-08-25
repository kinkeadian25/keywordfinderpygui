import os
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Keyword(Base):
    __tablename__ = 'keywords'

    id = Column(Integer, primary_key=True)
    prefix = Column(String)
    keyword = Column(String)

engine = create_engine('sqlite:///keywords.db')
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

if not session.query(Keyword).first():
    default_keywords = [
        Keyword(prefix='cat', keyword='meow'),
        Keyword(prefix='dog', keyword='bark'),
        Keyword(prefix='pet', keyword='food')
    ]
    session.add_all(default_keywords)
    session.commit()

def update_keywords():
    keywords = {}
    for kw in session.query(Keyword).all():
        if kw.prefix not in keywords:
            keywords[kw.prefix] = []
        keywords[kw.prefix].append(kw.keyword)
    return keywords

def search_files(directory, keywords):
    results = {}
    for filename in os.listdir(directory):
        prefix = filename[:3]
        if prefix in keywords:
            with open(os.path.join(directory, filename), 'r') as file:
                for line in file:
                    if any(keyword in line for keyword in keywords[prefix]):
                        if prefix not in results:
                            results[prefix] = []
                        results[prefix].append(line.strip())
    return results

def update_keyword_in_db(category, keyword):
    new_keyword = Keyword(prefix=category, keyword=keyword)
    session.add(new_keyword)
    session.commit()
