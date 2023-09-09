from sqlalchemy import inspect, Table, MetaData
from sqlalchemy import func
from werkzeug.security import check_password_hash
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import IntegrityError

from datetime import datetime, timedelta
from models import SessionLocal, Users, MindState

# For type hints
from typing import Type, List, Optional
from sqlalchemy.ext.declarative import declarative_base as DeclarativeBase

TableType = Type[DeclarativeBase]


from sqlalchemy import func


# Authenticating user with database
def authenticate(email: str, password: str) -> bool:
    with SessionLocal() as session:
        try:
            user_in_db = session.query(Users).filter_by(email=email).one()
            if check_password_hash(user_in_db.password, password):
                return True
        except NoResultFound:
            pass
    return False


def create_user(email: str, name: str, hashed_password: str) -> Users:
    new_user = Users(email=email, name=name, password=hashed_password)

    with SessionLocal() as session:
        session.add(new_user)
        try:
            session.commit()
        except IntegrityError:  # This handles cases where email is not unique
            session.rollback()
            raise ValueError(f"A user with email {email} already exists.")

    return new_user


def delete_user(user_id: int) -> None:
    with SessionLocal() as session:
        user = session.query(Users).filter(Users.id == user_id).one_or_none()

        if not user:
            raise ValueError(f"No user found with ID: {user_id}")

        session.delete(user)
        session.commit()


def get_user_name(user_id: int) -> str:
    with SessionLocal() as session:
        user = session.query(Users).filter(Users.id == user_id).one_or_none()
        if user:
            return user.name
        else:
            raise ValueError(f"No user found with ID: {user_id}")


def populate_mindstate(column: str, info: str, user_id: int):
    with SessionLocal() as session:
        # attempt to update existing row
        affected_rows = (
            session.query(MindState)
            .filter(MindState.user_id == user_id)
            .update({column: info})  # update can take a dictionary
        )

        if affected_rows == 0:
            # if no rows were affected, create a new record
            new_mind_state = MindState(
                user_id=user_id, **{column: info}
            )  # need to unpack the dictionary when intialising class
            session.add(new_mind_state)

        session.commit()
