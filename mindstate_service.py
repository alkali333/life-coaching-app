from models import Users, MindState
import json
from sqlalchemy.orm import Session


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
                data["MindState"][col_name] = col_value

        return json.dumps(data)

    def populate_mindstate(self, info: str, column: str) -> str:
        # attempt to update existing row
        affected_rows = (
            self.db.query(MindState)
            .filter(MindState.user_id == self.user_id)
            .update({column: info})  # update can take a dictionary
        )

        self.db.commit()

        if affected_rows == 0:
            # if no rows were affected, create a new record
            new_mind_state = MindState(
                user_id=self.user_id, **{column: info}
            )  # need to unpack the dictionary when initializing class
            self.db.add(new_mind_state)
            self.db.commit()

        # Update the self.mind_state attribute
        self.mind_state = (
            self.db.query(MindState).filter(MindState.user_id == self.user_id).first()
        )

        # return JSON of updated MindState
        return self.to_json()

    def get_hopes_and_dreams(self) -> str:
        return self.mind_state.hopes_and_dreams

    def get_skills_and_achievements(self) -> str:
        return self.mind_state.skills_and_achievements

    def get_obstacles_and_challenges(self) -> str:
        return self.mind_state.obstacles_and_challenges

    def get_grateful_for(self) -> str:
        return self.mind_state.grateful_for

    def get_current_tasks(self) -> str:
        return self.mind_state.current_tasks
