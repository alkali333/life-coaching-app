import os
import stat
from sqlalchemy import Column, String, Date, Integer, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


Base = declarative_base()

class GoalsAndDreams(Base):
    __tablename__ = 'goals_and_dreams'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    description = Column(String)

class CurrentTasks(Base):
    __tablename__ = 'current_tasks'
    id = Column(Integer, primary_key=True, index=True)
    entry = Column(String)
    date = Column(Date)

class SkillsAndVirtues(Base):
    __tablename__ = 'skills_and_virtues'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)

class Obstacles(Base):
    __tablename__ = 'obstacles'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    cause = Column(String)

class GratitudeJournal(Base):
    __tablename__ = 'gratitude_journal'
    id = Column(Integer, primary_key=True, index=True)
    entry = Column(String)
    date = Column(Date)

class VentingJournal(Base):
    __tablename__ = 'venting_journal'
    id = Column(Integer, primary_key=True, index=True)
    entry = Column(String)
    date = Column(Date)

class Tools(Base):
    __tablename__ = 'tools'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    description = Column(String)

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

