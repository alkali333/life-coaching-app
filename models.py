import os
import stat
from sqlalchemy import Column, Integer, String, ForeignKey, create_engine, Date
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import DateTime
from dotenv import load_dotenv

load_dotenv()


Base = declarative_base()


class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)
    email = Column(String, unique=True)
    password = Column(String(256))  # Hashed password column
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


SQLALCHEMY_DATABASE_URL = f'postgresql://{os.getenv("DATABASE_USERNAME")}:{os.getenv("DATABASE_PASSWORD")}@{os.getenv("DATABASE_HOSTNAME")}:{os.getenv("DATABASE_PORT")}/{os.getenv("DATABASE_NAME")}'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)
