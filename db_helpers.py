from sqlalchemy import inspect, Table, MetaData
from sqlalchemy.orm import Session
from models import SessionLocal


def fetch_and_format_data(table, columns, num_rows):
    # Create and manage the session
    with SessionLocal() as db_session:

        # If n is not specified, fetch all rows; otherwise, fetch the first n rows
        rows = db_session.query(table).limit(num_rows) if num_rows else db_session.query(table)

        # Format the data into the desired string
        formatted_string = ', '.join([f'{column.upper()}: {getattr(row, column)}' for row in rows for column in columns])

    return formatted_string
