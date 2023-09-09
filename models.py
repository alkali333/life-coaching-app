import os
import stat
from sqlalchemy import Column, Integer, String, ForeignKey, create_engine, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.orm import sessionmaker
from sqlalchemy import DateTime

Base = declarative_base()


class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)
    email = Column(String, unique=True)
    password = Column(String(100))  # Hashed password column
    is_new = Column(Integer, default=1)

    diary = relationship("Diary", back_populates="users")
    mind_state = relationship("MindState", back_populates="users")


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
    grateful_for = Column(String)
    current_tasks = Column(String)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True)
    timestamp = Column(DateTime)

    users = relationship("Users", back_populates="mind_state")


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
