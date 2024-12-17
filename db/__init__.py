from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models.base import Base

# 'sqlite:///fund.db'
global_engine = None

def create_engine_and_table(db_url):
    global global_engine
    global_engine = create_engine(db_url)

    Base.metadata.create_all(global_engine)



def get_session():
    session = sessionmaker(bind=global_engine)

    return session()

# get_session("sqlite:///C:/Users/Mayn/PycharmProjects/MeePass/database/meepass.db")




