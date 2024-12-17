from sqlalchemy import Column, Integer, String, ForeignKey

from models.base import Base


class Groups(Base):
    __tablename__ = 'groups'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    notes = Column(String)
    parent_id = Column(Integer, ForeignKey('groups.id'))