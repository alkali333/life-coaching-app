from dotenv import load_dotenv
import streamlit as st
from input_summarizer import InputSummarizer
from life_coach import LifeCoach
from mindstate_service import MindStateService
from models import SessionLocal
from exercises import create_random_prompt

load_dotenv()

# if "current_question" not in st.session_state:
#     st.session_state.current_question = 1

# input_summarizer = InputSummarizer()

### STEP ONE ###
if st.session_state.current_question == 1:
    st.write("Tell me about your hopes and dreams")
    with st.form(key="hopes", clear_on_submit=True):
        st.session_state.hopes_and_dreams = st.text_area("Your info")
        submit_button = st.form_submit_button("Go")

    if st.session_state.hopes_and_dreams and submit_button:
        with st.spinner("Loading Summary... "):
            response = input_summarizer.summarize(st.session_state.hopes_and_dreams)
            with SessionLocal() as db:
                MindStateService.populate_mindstate(
                    user_id=1,
                    info=response.content,
                    db=db,
                    column="hopes_and_dreams",
                )
        st.session_state.current_question = 2
        st.experimental_rerun()

### STEP TWO ###
elif st.session_state.current_question == 2:
    st.write("Tell me about your skills and achievements")
    with st.form(key="skills", clear_on_submit=True):
        st.session_state.skills_and_achievements = st.text_area("Your info")
        submit_button = st.form_submit_button("Go")

    if st.session_state.skills_and_achievements and submit_button:
        with st.spinner("Loading Summary... "):
            response = input_summarizer.summarize(
                st.session_state.skills_and_achievements
            )
            with SessionLocal() as db:
                MindStateService.populate_mindstate(
                    user_id=1,
                    info=response.content,
                    db=db,
                    column="skills_and_achievements",
                )
        st.session_state.current_question = 3
        st.experimental_rerun()

### STEP THREE ###
elif st.session_state.current_question == 3:
    st.write("Tell me about your obstacles and challenges")
    with st.form(key="obstacles", clear_on_submit=True):
        st.session_state.obstacles_and_challenges = st.text_area("Your info")
        submit_button = st.form_submit_button("Go")

    if st.session_state.obstacles_and_challenges and submit_button:
        with st.spinner("Loading Summary... "):
            response = input_summarizer.summarize(
                st.session_state.obstacles_and_challenges
            )
            with SessionLocal() as db:
                st.session_state.mindstate = MindStateService.populate_mindstate(
                    user_id=1,
                    info=response.content,
                    db=db,
                    column="obstacles_and_challenges",
                )
        st.session_state.current_question = 4
        st.experimental_rerun()

elif st.session_state.current_question == 4:

# get mindstate from the database
with SessionLocal() as db:
    mindstate = MindStateService.to_json(db=db, user_id=1)

# create a life coach
my_life_coach = LifeCoach(mindstate=mindstate)

prompt = create_random_prompt()

response = my_life_coach.create_exercise(prompt)

st.write(response.content)
