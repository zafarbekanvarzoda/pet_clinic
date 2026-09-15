from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship,  declarative_base
from database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    phone = Column(String)
    address = Column(String)

    owner = relationship("Owner", back_populates="user", uselist=False)


owner_vet = Table(
    "owner_vet",
    Base.metadata,
    Column(
        "owner_id",
        Integer,
        ForeignKey("owners.id"),
        primary_key = True),

    Column(
        "vet_id",
        Integer,
        ForeignKey("vets.id"),
        primary_key = True),
    )





class Owner(Base):
    __tablename__ = "owners"
    id = Column(Integer, primary_key=True)

    user_id = Column(Integer, ForeignKey("users.id"))

    user = relationship("User", back_populates="owner")
    pets = relationship("Pet", back_populates="owner")
    vets = relationship("Vet", secondary = owner_vet,  back_populates="owners")



class Pet(Base):
    __tablename__ = "pets"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    species = Column(String)
    age = Column(Integer)
    diagnosis = Column(String)

    owner_id = Column(Integer, ForeignKey("owners.id"))
    vet_id = Column(Integer, ForeignKey("vets.id"))

    owner = relationship("Owner", back_populates="pets")
    vet = relationship("Vet", back_populates="pets")


class Vet(Base):
    __tablename__ = "vets"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    services = Column(String)

    pets = relationship("Pet", back_populates="vet")
    owners = relationship("Owner", secondary=owner_vet,back_populates="vets")



