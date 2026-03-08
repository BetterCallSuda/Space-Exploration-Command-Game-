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


