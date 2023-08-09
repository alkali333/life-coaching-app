from sqlalchemy import inspect, Table, MetaData
from sqlalchemy import func

from datetime import datetime, timedelta
from models import SessionLocal, GratitudeJournal, CurrentProjects, Users


def fetch_and_format_data(user_id, table, columns, num_rows):
    # Create and manage the session
    with SessionLocal() as db_session:

        # Fetch rows in descending order of id because latest entries will have highest id
        query = db_session.query(table).filter_by(user_id=user_id).order_by(table.id.desc())

        # If n is specified, fetch the last n rows; otherwise, fetch all rows
        rows = query.limit(num_rows) if num_rows else query.all()

        # Format the data into the desired string
        formatted_string = ', '.join([f'{column.upper()}: {getattr(row, column)}' for row in rows for column in columns])

    return formatted_string

def diary_updated(user_id):
    two_days_ago = (datetime.now() - timedelta(days=2)).date()

    with SessionLocal() as session:
        # Check the latest entry for GratitudeJournal
        latest_gratitude_entry = session.query(func.max(GratitudeJournal.date)).filter_by(user_id=user_id).scalar()
        
        # Check the latest entry for CurrentProjects
        latest_project_entry = session.query(func.max(CurrentProjects.date)).filter_by(user_id=user_id).scalar()

    # Return True if both diaries have entries within the last two days, else return False
    # Also works if there are no entries
    return (latest_gratitude_entry and latest_gratitude_entry >= two_days_ago) and \
           (latest_project_entry and latest_project_entry >= two_days_ago)

def get_user_name(user_id):
    with SessionLocal() as session:
        user = session.query(Users).filter(Users.id == user_id).one_or_none()
        if user:
            return user.name
        else:
            raise ValueError(f"No user found with ID: {user_id}")
