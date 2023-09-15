import streamlit as st
from langchain.chat_models import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage, AIMessage

from datetime import date, datetime
from dotenv import load_dotenv, find_dotenv
import pandas as pd
from sqlalchemy import desc
import random

# My imports
from models import (
    Users,
    SessionLocal,
    MindState,
    Diary,
)


from db_helpers import authenticate
from life_coach import LifeCoach
from mindstate_service import MindStateService
from input_summarizer import InputSummarizer
from exercises import create_random_meditation
from quotes import get_random_quote


from polly import text_to_speech


load_dotenv(find_dotenv(), override=True)


# used when database updated, this will get the latest user mindstate
# and update the life_coach object
def refresh_life_coach():
    with SessionLocal() as db:
        st.session_state.life_coach.reset_mindstate(
            st.session_state.mindstate_service.to_json()
        )


# grab a quote
if "quote" not in st.session_state:
    st.session_state.quote = get_random_quote()

if "new_user" not in st.session_state:
    st.session_state.new_user = False


if "user_id" not in st.session_state:
    email = st.sidebar.text_input("Email", value="")
    password = st.sidebar.text_input("Password", type="password")

    if st.sidebar.button("Login"):
        if authenticate(email, password):
            # once authenticated we will store the user_id, user_name, mindstate_service, and life_coach
            # as session variables, and also determine if the user is new
            with SessionLocal() as session:
                user_in_db = session.query(Users).filter_by(email=email).first()

            st.session_state.user_id = user_in_db.id
            # store user name
            st.session_state.user_name = user_in_db.name
            # record if the user is new
            st.session_state.new_user = bool(user_in_db.is_new)

            # store mindstate service (so we can update and display MindState)
            st.session_state.mindstate_service = MindStateService(
                user_id=st.session_state.user_id, db=session
            )

            # load the mindstate as json string
            user_mindstate = st.session_state.mindstate_service.to_json()

            # create lifecoach
            st.session_state.life_coach = LifeCoach(user_mindstate)

        else:
            st.sidebar.text("Authentication failed. Please check your credentials.")
else:
    st.header("Atenshun v0.3 :black_heart: :brain: :old_key: ")

    st.write(
        f"<strong>Welcome, {st.session_state.user_name}!</strong>",
        unsafe_allow_html=True,
    )
    st.write(f"{st.session_state.quote}")

    if "welcome_message" not in st.session_state:
        # sets the welcome message to generic or customised depending on if the user is new
        if st.session_state.new_user:
            with st.spinner("Loading your welcome message"):
                st.session_state.welcome_message = (
                    "Welcome! Please use the form to tell me about yourself. "
                )
        else:
            #
            prompts = [
                """Create an epic poem about the user as if they were a great warrior.
                    Use the info you have along with a little humour. Give them hope that they
                    can defeat their obstacles and manifest their hopes and dreams""",
                """give the user 5 missions for today that will help them achieve their hopes and dreams, they can be small simple tasks""",
                """Recommend 3 random life-coaching exercises that will help them based on the user info """,
                """Offer the client some exercises they can do today to overcome their obstacles and challenges""",
                """Write a humourous epic fantasy/sci-fi adventure in a world of talking animals, robots, 
                    technology and magic. Make the client the main character (pick an unusual animal with strange characteristics) is a story that has them use their skills
                    and achievements to overcome their obstacles and challenges and reach all their hopes and dreams""",
            ]

            st.session_state.welcome_message = (
                st.session_state.life_coach.create_exercise(random.choice(prompts))
            )

    st.write(st.session_state.welcome_message)

    button_placeholder = st.empty()

    # initialise current question
    if "current_question" not in st.session_state:
        if st.session_state.new_user:
            st.session_state.current_question = 1
        else:
            st.session_state.current_question = 0

    st.write(
        f"debugging: current question is: {st.session_state.current_question} new user: {st.session_state.new_user}"
    )

    if st.session_state.current_question == 0:
        st.write(
            "Change is good. If you would like to tell me about yourself again, go ahead!"
        )
        with st.form(key="start"):
            submit_button = st.form_submit_button("Tell me about yourself")
        if submit_button:
            st.session_state.current_question = 1
            st.experimental_rerun()
    if st.session_state.current_question == 1:
        with st.form(key="hopes", clear_on_submit=True):
            st.write(
                "Let's get started. Tell me about your hopes and dreams. Don't be afraid to think big. Tell me at least 3."
            )

            hopes_and_dreams = st.text_area(
                label="Your hopes and dreams",
                placeholder=st.session_state.mindstate_service.get_hopes_and_dreams(),
                height=333,
            )
            submit_button = st.form_submit_button("Next")

            if hopes_and_dreams and submit_button:
                with st.spinner("Understanding your hopes and dreams.. "):
                    input_summarizer = InputSummarizer()
                    response = input_summarizer.summarize(hopes_and_dreams)

                st.session_state.mindstate_service.populate_mindstate(
                    info=response.content,
                    column="hopes_and_dreams",
                )
                st.session_state.current_question = 2
                st.experimental_rerun()

    elif st.session_state.current_question == 2:
        with st.form(key="skills", clear_on_submit=True):
            st.write("Tell me about your skills and achievements")

            skills_and_achievements = st.text_area(
                label="Your skills and achievements",
                placeholder=st.session_state.mindstate_service.get_skills_and_achievements(),
                height=333,
            )

            submit_button = st.form_submit_button("Next")

            if skills_and_achievements and submit_button:
                with st.spinner("Learning about your skills and achievements "):
                    input_summarizer = InputSummarizer()
                    response = input_summarizer.summarize(skills_and_achievements)

                st.session_state.mindstate_service.populate_mindstate(
                    info=response.content,
                    column="skills_and_achievements",
                )
                st.session_state.current_question = 3
                st.experimental_rerun()

    ### STEP THREE ###
    elif st.session_state.current_question == 3:
        st.write("Tell me about your obstacles and challenges")
        with st.form(key="obstacles", clear_on_submit=True):
            obstacles_and_challenges = st.text_area(
                label="Your obstacles and challenges",
                placeholder=st.session_state.mindstate_service.get_obstacles_and_challenges(),
                height=333,
            )

            submit_button = st.form_submit_button("Go")

        if obstacles_and_challenges and submit_button:
            with st.spinner("Getting to know your obstacles and challenges.... "):
                input_summarizer = InputSummarizer()
                response = input_summarizer.summarize(obstacles_and_challenges)
            st.session_state.mindstate_service.populate_mindstate(
                info=response.content,
                column="obstacles_and_challenges",
            )
            print("Obstacles and challenges updated")
            with SessionLocal() as session:
                # Get the user instance
                user = (
                    session.query(Users)
                    .filter(Users.id == st.session_state.user_id)
                    .one()
                )
                # reset the life coach to have the new info
                refresh_life_coach()
                print(f"Form finished, user:{user} retrieved from the database")

                if user.is_new == 1:
                    print("User is new, setting user to not new....")
                    user.is_new = 0
                    session.commit()

                    # Fetch the user again to confirm the update
                    user_after_update = (
                        session.query(Users)
                        .filter(Users.id == st.session_state.user_id)
                        .one()
                    )
                    if user_after_update.is_new == 0:
                        print("Successfully updated user to not new in the database.")
                        st.session_state.new_user = False
                    else:
                        print("Failed to update user status in the database.")
                else:
                    print("User is already not new.")

                st.session_state.current_question = 4
                st.experimental_rerun()

    elif st.session_state.current_question == 4:
        st.write(
            "Thanks for the info! Now start updating your gratitude diary and task list"
        )

    col3, col4 = st.columns(2)
    #
    ################## GRATITUDE JOURNAL
    if not st.session_state.new_user:
        with col3:
            st.subheader("Gratitude Journal")
            with SessionLocal() as session:
                latest_entry = (
                    session.query(MindState.grateful_for)
                    .filter(MindState.user_id == st.session_state.user_id)
                    .first()
                )

            st.write(
                f"Your most recent entry: \n\n{latest_entry[0] or 'No entries yet! Please update to access them meditations'}"
            )

            # Form to add new entries
            with st.form(key="gratitude_journal", clear_on_submit=True):
                entry = st.text_area("Entry")
                submit_button = st.form_submit_button(label="Submit")
                if submit_button:
                    with SessionLocal() as session:
                        st.session_state.mindstate_service.populate_mindstate(
                            info=entry,
                            column="grateful_for",
                        )
                        refresh_life_coach()
                        st.experimental_rerun()  # Rerun the app to refresh the data

        #
        ################## CURRENT TASKS
        #
        with col4:
            st.subheader("Current Missions")
            # Display existing data
            with SessionLocal() as session:
                current_tasks = (
                    session.query(MindState.current_tasks)
                    .filter(MindState.user_id == st.session_state.user_id)
                    .first()
                )
            st.write(
                f"Your most recent entry: \n\n{current_tasks[0] or 'No entries yet! Please update to access them meditations'}"
            )

            # Form to add new entries
            with st.form(key="current tasks", clear_on_submit=True):
                entry = st.text_area("Entry")
                submit_button = st.form_submit_button(label="Submit")
                if submit_button:
                    with SessionLocal() as session:
                        st.session_state.mindstate_service.populate_mindstate(
                            info=entry,
                            column="current_tasks",
                        )
                        refresh_life_coach()
                        st.experimental_rerun()  # Rerun the app to refresh the data

    st.write("\n\n" * 11)
    st.write("-" * 777)
    if st.session_state.mindstate_service.was_updated_recently():
        st.write(
            f"Well done for keeping your gratitude journal and daily missions log up to date. You can now access the exercises and pep talks!"
        )

        text_placeholder = st.empty()
        audio_placeholder = st.empty()
        download_placeholder = st.empty()

        col5, col6, col7 = st.columns(3)
        with col5:
            if st.button("Random Exercise"):
                query = create_random_meditation("misc")
                response = st.session_state.life_coach.create_exercise(query=query)
                # text_placeholder.write(f"Exercise: {response}")
                audio_path = text_to_speech(
                    user_id=st.session_state.user_id, text=response
                )
                audio_placeholder.audio(audio_path)
                with open(audio_path, "rb") as file:
                    file_bytes = file.read()

                download_placeholder.download_button(
                    label="Download",
                    data=file_bytes,
                    file_name=f"random-{date.today().strftime('%Y-%m-%d')}.mp3",
                    mime="audio/mpeg",
                )
        with col6:
            if st.button("No Nonsense Pep Talk"):
                coach_info = """You are hard-hitting, no nonsense drill sergeant, like the one out of full metal jacket, very strict, you don't mince your words!
                                You don't want your solider to end up as a pathetic loser, you are going to shout at them until they get their act together! 
                                You will be asked to create exercises for the user, based only on the information provided below in JSON. Use their name in the exercises. """

                query = """Create a motivational talk for the user, explaining them how important it is to get their current tasks done. Point out to them that the tasks
                    are essential if they are going to fulfill their hopes and dreams """

                response = st.session_state.life_coach.create_exercise(
                    coach_info=coach_info, query=query
                )
                # text_placeholder.write(f"Exercise: {response}")
                audio_path = text_to_speech(
                    user_id=st.session_state.user_id, text=response
                )
                audio_placeholder.audio(audio_path)
                with open(audio_path, "rb") as file:
                    file_bytes = file.read()

                download_placeholder.download_button(
                    label="Download",
                    data=file_bytes,
                    file_name=f"random-{date.today().strftime('%Y-%m-%d')}.mp3",
                    mime="audio/mpeg",
                )
        with col7:
            if st.button("Manifest Your Dreams"):
                query = create_random_meditation("hopes_and_dreams")

                response = st.session_state.life_coach.create_exercise(query=query)
                # text_placeholder.write(f"Exercise: {response}")
                audio_path = text_to_speech(
                    user_id=st.session_state.user_id, text=response
                )
                audio_placeholder.audio(audio_path)
                with open(audio_path, "rb") as file:
                    file_bytes = file.read()

                download_placeholder.download_button(
                    label="Download",
                    data=file_bytes,
                    file_name=f"random-{date.today().strftime('%Y-%m-%d')}.mp3",
                    mime="audio/mpeg",
                )
        col9, col10, col11 = st.columns(3)
        with col9:
            if st.button("Boost your self-esteem"):
                query = create_random_meditation("skills_and_achievements")

                response = st.session_state.life_coach.create_exercise(query=query)
                text_placeholder.write(f"Exercise: {response}")
                audio_path = text_to_speech(
                    user_id=st.session_state.user_id, text=response
                )
                audio_placeholder.audio(audio_path)
                with open(audio_path, "rb") as file:
                    file_bytes = file.read()

                download_placeholder.download_button(
                    label="Download",
                    data=file_bytes,
                    file_name=f"random-{date.today().strftime('%Y-%m-%d')}.mp3",
                    mime="audio/mpeg",
                )
        with col10:
            if st.button("Self-EMPOWERMENT!"):
                query = create_random_meditation("empowerment")

                response = st.session_state.life_coach.create_exercise(query=query)
                text_placeholder.write(f"Exercise: {response}")
                audio_path = text_to_speech(
                    user_id=st.session_state.user_id, text=response
                )
                audio_placeholder.audio(audio_path)
                with open(audio_path, "rb") as file:
                    file_bytes = file.read()

                download_placeholder.download_button(
                    label="Download",
                    data=file_bytes,
                    file_name=f"random-{date.today().strftime('%Y-%m-%d')}.mp3",
                    mime="audio/mpeg",
                )
        with col11:
            if st.button("Get things done!"):
                query = create_random_meditation("current_tasks")

                response = st.session_state.life_coach.create_exercise(query=query)
                text_placeholder.write(f"Exercise: {response}")
                audio_path = text_to_speech(
                    user_id=st.session_state.user_id, text=response
                )
                audio_placeholder.audio(audio_path)
                with open(audio_path, "rb") as file:
                    file_bytes = file.read()

                download_placeholder.download_button(
                    label="Download",
                    data=file_bytes,
                    file_name=f"random-{date.today().strftime('%Y-%m-%d')}.mp3",
                    mime="audio/mpeg",
                )

        ################## COACHING SESSIONS
        #

        st.write("\n\n" * 11)
        st.write("-" * 777)

        st.subheader("Plan Your Dreams")

        st.write("Goal Setting Exercise")

        if "messages" not in st.session_state:
            with st.form(key="goal_setting", clear_on_submit=True):
                goal_string = st.text_area(
                    "Enter a goal to get started. Use as much detail as you like."
                )
                goal_button = st.form_submit_button("Guide me to my goal!")
        if goal_button:
            st.session_state.messages = []

            system_message = f"""You are a life coach, guiding a client, {st.session_state.user_name}, through a goal-setting exercise using the SMART framework.

                The goal is:{goal_string}

                You will guide the user through each of the 5 steps separately for their goal. So first you will ask them to make their goals specific and so on.
                Once you have made the final summary of the SMART steps, don't ask any more questions but provide a lists of tasks for the user based on their responses and your insights """

            st.session_state.messages.append(SystemMessage(content=system_message))
            st.session_state.messages.append(HumanMessage(content="Let's get started"))

            chat = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0.7)

            response = chat(st.session_state.messages)
            st.session_state.messages.append(AIMessage(content=response.content))

        # if the chat is going on
        if "messages" in st.session_state:
            # print the latest response
            message_placeholder = st.empty()
            audio_placeholder = st.empty()

            with st.form(key="chat", clear_on_submit=True):
                user_chat_input = st.text_area(label="Send a message")
                chat_button = st.form_submit_button(label="Chat")

            if chat_button and user_chat_input:
                # append new input, get response, append chat response
                st.session_state.messages.append(HumanMessage(content=user_chat_input))
                chat = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0.7)
                response = chat(st.session_state.messages)
                st.session_state.messages.append(AIMessage(content=response.content))

            final_message = st.session_state.messages[-1].content
            if len(st.session_state.messages) == 13:
                final_message = (
                    final_message
                    + """ . Remember, you can add this list of suggestions to
                    your current task diary above. Keep your diaries updated to access these coaching exercises."""
                )

            st.write(f"MESSAGE COUNTER: {len(st.session_state.messages)}")
            message_placeholder.write(final_message)

            audio_path = text_to_speech(
                user_id=st.session_state.user_id, text=final_message
            )

            # Open the audio file using the returned path and play it in the placeholder
            with open(audio_path, "rb") as audio_file:
                audio_bytes = audio_file.read()
                audio_placeholder.audio(audio_bytes, format="audio/mp3")

    else:
        "Please make sure your gratitude diary and daily task list is up to date if you want access to the exercises and talks!"
    #
    ######## Dairy
    #

    st.write("\n\n" * 11)
    st.write("-" * 777)

    st.write(
        """This is your diary, you can write whatever you want here. Thoughs, hopes, fears, your progress - random nonsense. 
                Don't worry, you don't have to read it, but your army of AI coaches may take a look to keep you on track!"""
    )

    with st.form(key="diary", clear_on_submit=True):
        diary_entry = st.text_area("Entry")
        diary_submit_button = st.form_submit_button(label="Enter")

        if diary_submit_button:
            with SessionLocal() as session:
                new_entry = Diary(
                    entry=diary_entry,
                    date=datetime.today().date(),
                    user_id=st.session_state.user_id,
                )
                session.add(new_entry)
                session.commit()
            st.write("Diary Updated!")
