from sqlalchemy import inspect, Table, MetaData
from sqlalchemy.orm import Session
from models import SessionLocal


def fetch_and_format_data(table, columns, num_rows):
    # Create and manage the session
    with SessionLocal() as db_session:

        # Fetch rows in descending order of id because latest entries will have highest id
        query = db_session.query(table).order_by(table.id.desc())

        # If n is specified, fetch the last n rows; otherwise, fetch all rows
        rows = query.limit(num_rows) if num_rows else query.all()

        # Format the data into the desired string
        formatted_string = ', '.join([f'{column.upper()}: {getattr(row, column)}' for row in rows for column in columns])

    return formatted_string

