import random
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker, relationship

# ----------------------------
# DATABASE SETUP
# ----------------------------

Base = declarative_base()

engine = create_engine("sqlite:///space_game.db")
Session = sessionmaker(bind=engine)
session = Session()



# ----------------------------
# DATABASE MODELS
# ----------------------------

class Captain(Base):
    __tablename__ = "captains"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    ship_name = Column(String)
    fuel = Column(Integer)

    resources = relationship("Resource", back_populates="captain")

class Planet(Base):
    __tablename__ = "planets"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    danger_level = Column(Integer)


class Resource(Base):
    __tablename__ = "resources"

    id = Column(Integer, primary_key=True)
    resource_name = Column(String)
    quantity = Column(Integer)

    captain_id = Column(Integer, ForeignKey("captains.id"))
    captain = relationship("Captain", back_populates="resources")


class Mission(Base):
    __tablename__ = "missions"

    id = Column(Integer, primary_key=True)
    planet_name = Column(String)
    result = Column(String)
    captain_name = Column(String)


Base.metadata.create_all(engine)


# ----------------------------
# CREATE PLANETS
# ----------------------------

def create_planets():

    if session.query(Planet).count() == 0:

        planets = [
            Planet(name="Mars", danger_level=2),
            Planet(name="Titan", danger_level=3),
            Planet(name="Zerion", danger_level=5),
            Planet(name="Nebula-X", danger_level=4)
        ]

        session.add_all(planets)
        session.commit()

