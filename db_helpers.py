from sqlalchemy import inspect, Table, MetaData
from sqlalchemy import func
from werkzeug.security import check_password_hash
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import IntegrityError

from datetime import datetime, timedelta
from models import SessionLocal, GratitudeJournal, CurrentProjects, Users

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


from typing import List


def fetch_and_format_data(
    user_id: int,
    table: TableType,
    columns: List[str],
    num_rows: int = None,
    random: bool = False,
    id: int = None,
) -> str:
    # Create and manage the session
    with SessionLocal() as db_session:
        # Start the query
        query = db_session.query(table).filter_by(user_id=user_id)

        # Apply ordering
        if random:
            query = query.order_by(func.random())  # Use func.rand() for MySQL
        else:
            query = query.order_by(table.id.desc())

        if id:
            query = query.filter_by(id=id)

        # If n is specified, fetch the last n rows; otherwise, fetch all rows
        rows = query.limit(num_rows) if num_rows else query.all()

        # Check if the query returned any rows
        if not rows:
            return "    No specific entries yet"

        # Format the data into the desired string
        formatted_string = ", ".join(
            [
                f"{column.upper()}: {getattr(row, column)}"
                for row in rows
                for column in columns
            ]
        )

    return formatted_string


def diary_updated(user_id: int) -> bool:
    two_days_ago = (datetime.now() - timedelta(days=2)).date()

    with SessionLocal() as session:
        # Check the latest entry for GratitudeJournal
        latest_gratitude_entry = (
            session.query(func.max(GratitudeJournal.date))
            .filter_by(user_id=user_id)
            .scalar()
        )

        # Check the latest entry for CurrentProjects
        latest_project_entry = (
            session.query(func.max(CurrentProjects.date))
            .filter_by(user_id=user_id)
            .scalar()
        )

    # Return True if both diaries have entries within the last two days, else return False
    # Also works if there are no entries
    return (latest_gratitude_entry and latest_gratitude_entry >= two_days_ago) and (
        latest_project_entry and latest_project_entry >= two_days_ago
    )


def get_user_name(user_id: int) -> str:
    with SessionLocal() as session:
        user = session.query(Users).filter(Users.id == user_id).one_or_none()
        if user:
            return user.name
        else:
            raise ValueError(f"No user found with ID: {user_id}")
