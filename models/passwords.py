from sqlalchemy import Column, String, Integer, ForeignKey

from models.base import Base


class Passwords(Base):
    __tablename__ = 'passwords'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String)
    username = Column(String)
    password = Column(String)
    url = Column(String)
    notes = Column(String)
    group_id = Column(Integer, ForeignKey('groups.id'))