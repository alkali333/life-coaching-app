import os
import stat
from sqlalchemy import Column, Integer, String, ForeignKey, create_engine, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.orm import sessionmaker


Base = declarative_base()


class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)
    email = Column(String, unique=True)
    password = Column(String(100))  # Hashed password column

    # Define the one-to-many relationships
    goals_and_dreams = relationship("GoalsAndDreams", back_populates="users")
    powers_and_achievements = relationship(
        "PowersAndAchievements", back_populates="users"
    )
    gratitude_journal = relationship("GratitudeJournal", back_populates="users")
    current_projects = relationship("CurrentProjects", back_populates="users")
    diary = relationship("Diary", back_populates="users")
    mind_state = relationship("MindState", back_populates="users")


class GoalsAndDreams(Base):
    __tablename__ = "goals_and_dreams"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    description = Column(String)
    user_id = Column(Integer, ForeignKey("users.id"))

    users = relationship("Users", back_populates="goals_and_dreams")


class PowersAndAchievements(Base):
    __tablename__ = "powers_and_achievements"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    description = Column(String)
    user_id = Column(Integer, ForeignKey("users.id"))

    users = relationship("Users", back_populates="powers_and_achievements")


class GratitudeJournal(Base):
    __tablename__ = "gratitude_journal"
    id = Column(Integer, primary_key=True, index=True)
    entry = Column(String)
    date = Column(Date)
    user_id = Column(Integer, ForeignKey("users.id"))

    users = relationship("Users", back_populates="gratitude_journal")


class CurrentProjects(Base):
    __tablename__ = "current_projects"
    id = Column(Integer, primary_key=True, index=True)
    entry = Column(String)
    date = Column(Date)
    user_id = Column(Integer, ForeignKey("users.id"))

    users = relationship("Users", back_populates="current_projects")


class Diary(Base):
    __tablename__ = "diary"
    id = Column(Integer, primary_key=True, index=True)
    entry = Column(String)
    date = Column(Date)
    user_id = Column(Integer, ForeignKey("users.id"))

    users = relationship("Users", back_populates="diary")


class MindState(Base):
    __tablename__ = "mind_state"
    id = Column(Integer, primary_key=True, index=True)
    hopes_and_dreams = Column(String)
    skills_and_achievements = Column(String)
    obstacles_and_challenges = Column(String)
    current_missions = Column(String)
    grateful_for = Column(String)
    current_tasks = Column(String)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True)

    users = relationship("Users", back_populates="mind_state")


# class Obstacles(Base):
#     __tablename__ = 'obstacles'
#     id = Column(Integer, primary_key=True, index=True)
#     name = Column(String)
#     cause = Column(String)


# class VentingJournal(Base):
#     __tablename__ = 'venting_journal'
#     id = Column(Integer, primary_key=True, index=True)
#     entry = Column(String)
#     date = Column(Date)

# class Tools(Base):
#     __tablename__ = 'tools'
#     id = Column(Integer, primary_key=True, index=True)
#     name = Column(String)
#     description = Column(String)

# Ensure the directory exists
DATABASE_DIR = "database"
if not os.path.exists(DATABASE_DIR):
    os.makedirs(DATABASE_DIR)

# Use the directory in your database URL
DATABASE_URL_PATH = os.path.join(DATABASE_DIR, "coaching.db")
DATABASE_URL = f"sqlite:///{DATABASE_URL_PATH}"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

# Create tables if they don't exist
Base.metadata.create_all(bind=engine)


# Set database permissions
def set_database_permissions(db_path):
    os.chmod(db_path, stat.S_IRUSR | stat.S_IWUSR | stat.S_IRGRP | stat.S_IWGRP)


set_database_permissions(DATABASE_URL_PATH)
