from langchain.agents import Tool, tool
from models import SessionLocal
from mindstate_service import MindStateService


# tools can return direct! So they can break the agent loop.
@tool
def get_hopes_and_dreams() -> str:
    """Useful when looking up the clients hopes and dreams"""
    with SessionLocal() as db:
        mss = MindStateService(user_id=1, db=db)
    return mss.get_hopes_and_dreams()


@tool
def get_skills_and_achievements() -> str:
    """Useful when looking up a client's skills and achievements"""
    with SessionLocal() as db:
        mss = MindStateService(user_id=1, db=db)
    return mss.get_skills_and_achievements()


@tool
def get_obstacles_and_challenges() -> str:
    """Useful when looking up a client's obstacles and challenges"""
    with SessionLocal() as db:
        mss = MindStateService(user_id=1, db=db)
    return mss.get_obstacles_and_challenges()


@tool
def get_grateful_for() -> str:
    """Useful when looking up what the client is grateful for"""
    with SessionLocal() as db:
        mss = MindStateService(user_id=1, db=db)
    return mss.get_grateful_for()


@tool
def get_current_tasks() -> str:
    """Useful when looking up a client's current tasks"""
    with SessionLocal() as db:
        mss = MindStateService(user_id=1, db=db)
    return mss.get_current_tasks()
