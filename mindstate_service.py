from models import Users, MindState
import json
from sqlalchemy.orm import Session
from datetime import datetime, timedelta


class MindStateService:
    user_id: int
    db: Session
    user_name: str
    mind_state: MindState

    def __init__(self, user_id: int, db: Session):
        self.user_id = user_id
        self.db = db
        user = self.db.query(Users).filter(Users.id == self.user_id).first()
        if not user:
            raise Exception(f"No user found for user_id: {self.user_id}")
        self.user_name = user.name

        self.mind_state = (
            self.db.query(MindState).filter(MindState.user_id == self.user_id).first()
        )
        if not self.mind_state:
            new_mind_state = MindState(user_id=self.user_id)
            self.db.add(new_mind_state)
            self.db.commit()
            self.mind_state = new_mind_state

    def to_json(self):
        # Prepare the data for JSON
        data = {"Client Name": self.user_name, "MindState": {}}

        for column in MindState.__table__.columns:
            col_name = column.name.replace("_", " ")
            col_value = getattr(self.mind_state, column.name)
            if col_value:
                if isinstance(col_value, datetime):
                    col_value = col_value.isoformat()  # Convert datetime to string
                data["MindState"][col_name] = col_value

        return json.dumps(data)

    def populate_mindstate(self, info: str, column: str) -> str:
        update_dict = {column: info}

        # Update the timestamp if the column is grateful_for or current_tasks
        if column in ["grateful_for", "current_tasks"]:
            update_dict["timestamp"] = datetime.now()

        # attempt to update existing row
        affected_rows = (
            self.db.query(MindState)
            .filter(MindState.user_id == self.user_id)
            .update(update_dict)
        )

        self.db.commit()

        if affected_rows == 0:
            # if no rows were affected, create a new record
            new_mind_state = MindState(user_id=self.user_id, **update_dict)
            self.db.add(new_mind_state)
            self.db.commit()

        # Update the self.mind_state attribute
        self.mind_state = (
            self.db.query(MindState).filter(MindState.user_id == self.user_id).first()
        )

        # return JSON of updated MindState
        return self.to_json() or ""

    def was_updated_recently(self) -> bool:
        two_days_ago = datetime.now() - timedelta(days=2)

        # Fetch the mind state entry for the user
        user_mind_state = (
            self.db.query(MindState).filter(MindState.user_id == self.user_id).first()
        )

        # If there's no record for the user or if the timestamp is None, return False
        if not user_mind_state or user_mind_state.timestamp is None:
            return False

        # Compare the timestamp to two_days_ago
        return user_mind_state.timestamp > two_days_ago

    def get_hopes_and_dreams(self) -> str:
        return self.mind_state.hopes_and_dreams or ""

    def get_skills_and_achievements(self) -> str:
        return self.mind_state.skills_and_achievements or ""

    def get_obstacles_and_challenges(self) -> str:
        return self.mind_state.obstacles_and_challenges or ""

    def get_grateful_for(self) -> str:
        return self.mind_state.grateful_for or ""

    def get_current_tasks(self) -> str:
        return self.mind_state.current_tasks or ""
