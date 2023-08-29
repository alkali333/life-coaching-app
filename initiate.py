from dotenv import load_dotenv
from db_helpers import populate_mindstate

import streamlit as st


from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.schema import HumanMessage, SystemMessage
from langchain.output_parsers import PydanticOutputParser


from pydantic import BaseModel, Field, validator
from typing import List


class MindState(BaseModel):
    heading: str
    summary: str


output_parser = PydanticOutputParser(pydantic_object=MindState)

load_dotenv()

# hardcode for one user for now
if "user_id" not in st.session_state:
    st.session_state.user_id = 1

with st.form(key="mind_state", clear_on_submit=True):
    info = st.text_area("Your info")
    submit_button = st.form_submit_button("Go")

if info and submit_button:
    st.write("Sending response to the LLM")
    output_parser = PydanticOutputParser(pydantic_object=MindState)

    prompt = PromptTemplate(
        template="""You are a life coach. The user (called {name}) is going to tell you something about their life (it could be their hopes and dreams, it could be their obstacles and challenges).
                    For each issue they bring up, you are to provide a heading and a single sentance summary, number each item. \n\n""",
        input_variables=["name"],
        # partial_variables={
        #     "format_instructions": output_parser.get_format_instructions()
        # },
    )

    formatted_message = prompt.format_prompt(name="Jake")

    llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0.7, max_tokens=1024)
    messages = [
        SystemMessage(content=str(formatted_message)),
        HumanMessage(content=info),
    ]

    with st.spinner("Loading Your message"):
        response = llm(messages)

    st.write(response.content)

    st.write("Inserting into database.... ")
    # maybe an agent can figure out which table to update?
    populate_mindstate(
        column="skills_and_achievements",
        info=response.content,
        user_id=st.session_state.user_id,
    )
    st.write("Done")
