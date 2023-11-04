from werkzeug.security import check_password_hash
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import OperationalError


def retry_db_operation(db, operation, *args, **kwargs):
    for attempt in range(5):  # Limit to 5 attempts
        try:
            result = operation(*args, **kwargs)
            db.commit()
            return result  # Return the result if operation was successful
        except OperationalError as e:  # Catch OperationalError exceptions
            print(f"Attempt {attempt + 1} failed with error: {e}")
            if attempt == 4:  # After 5 attempts, re-raise the exception
                raise
    return None  # Optional, return None if operation was unsuccessful after 5 attempts


# Authenticating user with database
def authenticate(session, table, email: str, password: str) -> bool:
    try:
        user_in_db = session.query(table).filter_by(email=email).one()
        if check_password_hash(user_in_db.password, password):
            return True
    except NoResultFound:
        pass
    return False
