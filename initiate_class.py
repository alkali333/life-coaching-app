from dotenv import load_dotenv
from langchain.chat_models import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage
import streamlit as st

from models import MindState, SessionLocal
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.schema import AIMessage, HumanMessage, SystemMessage
from langchain.output_parsers import PydanticOutputParser

load_dotenv()

# hardcode for one user for now
if "user_id" not in st.session_state:
    st.session_state.user_id = 1


class MindStateUpdater:
    def __init__(self, db_session, table, db_column, prompt_template):
        self.db_session = db_session
        self.table = table
        self.db_column = db_column
        self.prompt_template = prompt_template

    def populate_db(self, info, user_id):
        record = self.db_session.query(self.table).filter_by(user_id=user_id).first()
        if not record:
            record = self.table(user_id=user_id)
            self.db_session.add(record)
        setattr(record, self.db_column, info)
        self.db_session.commit()
        self.db_session.close()

    def handle_form(self, user_name, user_input):
        formatted_message = self.prompt_template.format_prompt(name=user_name)
        messages = [
            SystemMessage(content=str(formatted_message)),
            HumanMessage(content=user_input),
        ]

        llm = ChatOpenAI(temperature=0.7, model="gpt-3.5-turbo")

        response = llm(messages)
        return response.content


with st.form(key="mind_state", clear_on_submit=True):
    info = st.text_area("Your info")
    submit_button = st.form_submit_button("Go")

if info and submit_button:
    prompt = PromptTemplate(
        template="""You are a life coach. The user (called {name}) is going to tell you something about their life (it could be their hopes and dreams, it could be their obstacles and challenges).
                    For each issue they bring up, you are to provide a heading and a single sentance summary \n\n""",
        input_variables=["name"],
    )

    db_session = SessionLocal()
    mind_state_updater = MindStateUpdater(
        db_session=db_session,
        table=MindState,
        db_column="hopes_and_dreams",
        prompt_template=prompt,
    )
    with st.spinner("Loading Your Response"):
        response = mind_state_updater.handle_form(user_name="Jake", user_input=info)

    st.write(response)
    mind_state_updater.populate_db(info=response, user_id=st.session_state.user_id)
