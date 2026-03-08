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


# ----------------------------
# CREATE CAPTAIN
# ----------------------------

def create_captain():

    name = input("Enter Captain Name: ")
    ship = input("Enter Ship Name: ")

    captain = Captain(
        name=name,
        ship_name=ship,
        fuel=100
    )

    session.add(captain)
    session.commit()

    print("\nWelcome Captain", name)

    return captain


# ----------------------------
# SHOW RESOURCES
# ----------------------------

def show_resources(captain):

    items = session.query(Resource).filter_by(captain_id=captain.id).all()

    print("\n---- RESOURCES ----")

    if not items:
        print("No resources collected")

    for item in items:
        print(item.resource_name, "x", item.quantity)

    print("-------------------")


# ----------------------------
# ADD RESOURCE
# ----------------------------

def add_resource(captain, name, amount):

    item = session.query(Resource).filter_by(
        captain_id=captain.id,
        resource_name=name
    ).first()

    if item:
        item.quantity += amount
    else:
        item = Resource(
            resource_name=name,
            quantity=amount,
            captain_id=captain.id
        )
        session.add(item)

    session.commit()


# ----------------------------
# EXPLORE PLANET
# ----------------------------

def explore_planet(captain):

    if captain.fuel <= 0:
        print("\n⛽ No fuel left!")
        return

    planet = session.query(Planet).order_by(
        random.random()
    ).first()

    captain.fuel -= 10

    print("\n🚀 Traveling to:", planet.name)
    print("Danger Level:", planet.danger_level)

    event = random.choice(["resource", "alien", "storm"])

    if event == "resource":

        resource = random.choice(["Titanium", "Crystal", "Alien Tech"])
        amount = random.randint(5, 20)

        print("⛏ You found", amount, resource)

        add_resource(captain, resource, amount)

        result = "Resources collected"

    elif event == "alien":

        print("👽 Hostile aliens attacked!")

        damage = planet.danger_level * 5
        captain.fuel -= damage

        print("Fuel lost:", damage)

        result = "Alien encounter"

    else:

        print("🌪 Cosmic storm damaged ship")

        damage = random.randint(5, 15)
        captain.fuel -= damage

        print("Fuel lost:", damage)

        result = "Storm damage"

    mission = Mission(
        planet_name=planet.name,
        result=result,
        captain_name=captain.name
    )

    session.add(mission)
    session.commit()


# ----------------------------
# VIEW MISSIONS
# ----------------------------

def show_missions():

    missions = session.query(Mission).all()

    print("\n===== MISSION LOG =====")

    for m in missions:
        print(m.planet_name, "-", m.result, "-", m.captain_name)

    print("=======================")


# ----------------------------
# SHOW STATUS
# ----------------------------

def show_status(captain):

    print("\n---- SHIP STATUS ----")
    print("Captain:", captain.name)
    print("Ship:", captain.ship_name)
    print("Fuel:", captain.fuel)
    print("---------------------")


# ----------------------------
# GAME LOOP
# ----------------------------

def game_loop(captain):

    while True:

        print("\n===== SPACE COMMAND =====")
        print("1 Explore planet")
        print("2 Ship status")
        print("3 Resources")
        print("4 Mission log")
        print("5 Exit")

        choice = input("Select option: ")

        if choice == "1":
            explore_planet(captain)

        elif choice == "2":
            show_status(captain)

        elif choice == "3":
            show_resources(captain)

        elif choice == "4":
            show_missions()

        elif choice == "5":
            print("Mission ended. Safe travels Captain.")
            break

        else:
            print("Invalid option")


# ----------------------------
# START GAME
# ----------------------------

def main():

    create_planets()

    print("🚀 SPACE EXPLORER COMMAND")

    captain = create_captain()

    game_loop(captain)


if __name__ == "__main__":
    main()
