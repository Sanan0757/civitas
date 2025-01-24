# from enum import StrEnum

from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    # class Role(StrEnum):
    #     ADMIN = "admin"
    #     USER = "user"
    #     GUEST = "guest"


# one to one relationship
class Building(Base):
    __tablename__ = "buildings"


class BuildingDetail(Base):
    __tablename__ = "building_details"

    building_id = Column(Integer, ForeignKey("buildings.id"), primary_key=True)
    building = relationship("Building", back_populates="detail")
    detail = relationship("BuildingDetail", back_populates="building")
