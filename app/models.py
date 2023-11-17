import os
import stat
from sqlalchemy import Column, Integer, String, ForeignKey, create_engine, Date
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import DateTime
from dotenv import load_dotenv

from db_helpers import retry_db_operation

load_dotenv()


Base = declarative_base()


class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String, unique=True)
    password = Column(String(256))  # Hashed password column
    is_new = Column(Integer, default=1)

    diary = relationship("Diary", back_populates="user")
    mind_state = relationship("MindState", back_populates="user")


class Diary(Base):
    __tablename__ = "diary"
    id = Column(Integer, primary_key=True, index=True)
    entry = Column(String)
    summary = Column(String)
    date = Column(Date)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))

    user = relationship("Users", back_populates="diary")


class MindState(Base):
    __tablename__ = "mind_state"
    id = Column(Integer, primary_key=True, index=True)
    hopes_and_dreams = Column(String)
    skills_and_achievements = Column(String)
    obstacles_and_challenges = Column(String)
    grateful_for = Column(String)
    current_tasks = Column(String)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), unique=True)
    timestamp = Column(DateTime)

    user = relationship("Users", back_populates="mind_state")


# Check if 'DYNO' environment variable is set, as it is only set on Heroku
if "DYNO" in os.environ:
    # The app is on Heroku, use the DATABASE_URL environment variable
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")
else:
    if os.environ.get("SSLMODE") == "True":
        SQLALCHEMY_DATABASE_URL = f'postgresql://{os.getenv("DATABASE_USERNAME")}:{os.getenv("DATABASE_PASSWORD")}@{os.getenv("DATABASE_HOSTNAME")}:{os.getenv("DATABASE_PORT")}/{os.getenv("DATABASE_NAME")}?sslmode=require'
    else:
        SQLALCHEMY_DATABASE_URL = f'postgresql://{os.getenv("DATABASE_USERNAME")}:{os.getenv("DATABASE_PASSWORD")}@{os.getenv("DATABASE_HOSTNAME")}:{os.getenv("DATABASE_PORT")}/{os.getenv("DATABASE_NAME")}'

# Adjust these settings based on your requirements and observations
pool_size = 10  # Maximum number of connections
pool_timeout = 10  # Maximum time to wait for a connection
pool_recycle = 3600  # Maximum age of connections in seconds

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    pool_size=pool_size,
    pool_timeout=pool_timeout,
    pool_recycle=pool_recycle,
    pool_pre_ping=True,
)

engine = create_engine(SQLALCHEMY_DATABASE_URL, pool_pre_ping=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

# Add default user

with SessionLocal() as session:
    # Check if the user with ID 1 exists
    user_with_id_1 = session.query(Users).filter_by(id=1).first()

    if user_with_id_1 is None:
        # If default user doesn't exist, insert it
        new_user = Users(
            id=1,
            name="Jake",
            email="jake@alkalimedia.co.uk",
            password="pbkdf2:sha256:600000$HfEqpWbeavZrTMNl$9d7177999ac36590ea40c868699a8a972315806961c68610950a4fa9ab540028",
            is_new=1,
        )

        retry_db_operation(session, lambda: (session.add(new_user), session.commit()))
