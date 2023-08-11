import streamlit as st

from langchain.chat_models import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage, AIMessage


import streamlit_authenticator as stauth
from werkzeug.security import check_password_hash

from datetime import date, datetime
from dotenv import load_dotenv, find_dotenv
import pandas as pd
from sqlalchemy import desc

# My imports
from models import (
    GoalsAndDreams,
    GratitudeJournal,
    CurrentProjects,
    Users,
    PowersAndAchievements,
    SessionLocal,
)
from coaching_content import (
    morning_exercise,
    motivation_pep_talk,
    get_your_shit_together,
    blow_your_own_trumpet,
)

# The tables we want to work with
from db_helpers import diary_updated, fetch_and_format_data

load_dotenv(find_dotenv(), override=True)

from sqlalchemy.orm.exc import NoResultFound


# Authenticating user with database
def authenticate(email, password):
    with SessionLocal() as session:
        try:
            user_in_db = session.query(Users).filter_by(email=email).one()
            if check_password_hash(user_in_db.password, password):
                return True
        except NoResultFound:
            pass
    return False


if "user_id" not in st.session_state:
    email = st.sidebar.text_input("Email", value="jake@alkalimedia.co.uk")
    password = st.sidebar.text_input("Password", type="password")

    if st.sidebar.button("Login"):
        if authenticate(email, password):
            with SessionLocal() as session:
                user_in_db = session.query(Users).filter_by(email=email).first()
                if user_in_db:
                    st.session_state.user_id = user_in_db.id
                    st.session_state.user_name = (
                        user_in_db.name
                    )  # Storing the user's name in session state
                else:
                    st.sidebar.text(
                        "Unexpected error: User email found but not retrieved."
                    )
        else:
            st.sidebar.text("Authentication failed. Please check your credentials.")
else:
    st.write(
        f"Welcome, {st.session_state.user_name}!"
    )  # Greeting the user by their name

    col1, col2 = st.columns(2)
    #
    ################## GOALS AND DREAMS
    #
    with col1:
        st.subheader("Goals And Dreams")

        # Display existing data
        with SessionLocal() as session:
            existing_data = (
                session.query(GoalsAndDreams.name, GoalsAndDreams.description)
                .filter(GoalsAndDreams.user_id == st.session_state.user_id)
                .all()
            )
            existing_data_df = pd.DataFrame(
                existing_data, columns=["name", "description"]
            )
            existing_data_df.set_index("name", inplace=True)
            st.table(existing_data_df)

        # Count the number of existing entries
        count_records = len(existing_data)

        # Display form for new entry if less than 3 entries exist
        if count_records < 3:
            with st.form(key="goals_and_dreams", clear_on_submit=True):
                name = st.text_input("Name")
                description = st.text_input("Description")
                submit_button = st.form_submit_button(label="Submit")

                if submit_button:
                    with SessionLocal() as session:
                        new_goal = GoalsAndDreams(
                            name=name,
                            description=description,
                            user_id=st.session_state.user_id,
                        )
                        session.add(new_goal)
                        session.commit()
                        st.experimental_rerun()  # Rerun the app to refresh the data
        else:
            st.write("You've reached the limit of 3 entries.")

        if st.button("Clear All Entries"):
            with SessionLocal() as session:
                session.query(GoalsAndDreams).filter(
                    GoalsAndDreams.user_id == st.session_state.user_id
                ).delete()
                session.commit()
                st.experimental_rerun()  # Rerun the app to refresh the data

    #
    ################## POWERS AND ACHIEVEMENTS
    #
    with col2:
        st.subheader("Powers And Achievements")

        # Display existing data
        with SessionLocal() as session:
            existing_data = (
                session.query(
                    PowersAndAchievements.name, PowersAndAchievements.description
                )
                .filter(PowersAndAchievements.user_id == st.session_state.user_id)
                .all()
            )
            existing_data_df = pd.DataFrame(
                existing_data, columns=["name", "description"]
            )
            existing_data_df.set_index("name", inplace=True)
            st.table(existing_data_df)

        # Count the number of existing entries
        count_records = len(existing_data)

        # Display form for new entry if less than 3 entries exist
        if count_records < 5:
            with st.form(key="powers_and_achievements", clear_on_submit=True):
                name = st.text_input("Name")
                description = st.text_input("Description")
                submit_button = st.form_submit_button(label="Submit")

                if submit_button:
                    with SessionLocal() as session:
                        new_goal = PowersAndAchievements(
                            name=name,
                            description=description,
                            user_id=st.session_state.user_id,
                        )
                        session.add(new_goal)
                        session.commit()
                        st.experimental_rerun()  # Rerun the app to refresh the data
        else:
            st.write("You've reached the limit of 5 entries.")

        if st.button("Clear All Entries", key="clear_all_powers"):
            with SessionLocal() as session:
                session.query(PowersAndAchievements).filter(
                    PowersAndAchievements.user_id == st.session_state.user_id
                ).delete()
                session.commit()
                st.experimental_rerun()  # Rerun the app to refresh the data
    st.write("\n\n" * 11)
    st.write("-" * 777)
    col3, col4 = st.columns(2)
    #
    ################## GRATITUDE JOURNAL
    #
    with col3:
        st.subheader("Gratitude Journal")
        # Display existing data
        with SessionLocal() as session:
            existing_data = (
                session.query(GratitudeJournal.date, GratitudeJournal.entry)
                .filter(GratitudeJournal.user_id == st.session_state.user_id)
                .order_by(desc(GratitudeJournal.date))
                .limit(3)
                .all()
            )
            existing_data_df = pd.DataFrame(existing_data, columns=["date", "entry"])
            existing_data_df.set_index("date", inplace=True)
            st.dataframe(existing_data_df)

        # Form to add new entries
        with st.form(key="gratitude_journal", clear_on_submit=True):
            entry = st.text_area("Entry")
            submit_button = st.form_submit_button(label="Submit")
            if submit_button:
                with SessionLocal() as session:
                    new_entry = GratitudeJournal(
                        entry=entry,
                        date=datetime.today().date(),
                        user_id=st.session_state.user_id,
                    )
                    session.add(new_entry)
                    session.commit()
                    st.experimental_rerun()  # Rerun the app to refresh the data

    #
    ################## CURRENT TASKS
    #
    with col4:
        st.subheader("Current Tasks")
        # Display existing data
        with SessionLocal() as session:
            existing_data = (
                session.query(CurrentProjects.date, CurrentProjects.entry)
                .filter(CurrentProjects.user_id == st.session_state.user_id)
                .order_by(desc(CurrentProjects.date))
                .limit(3)
                .all()
            )
            existing_data_df = pd.DataFrame(existing_data, columns=["date", "entry"])
            existing_data_df.set_index("date", inplace=True)
            st.dataframe(existing_data_df)

        # Form to add new entries
        with st.form(key="current_tasks", clear_on_submit=True):
            entry = st.text_area("Entry")
            submit_button = st.form_submit_button(label="Submit")
            if submit_button:
                with SessionLocal() as session:
                    new_entry = CurrentProjects(
                        entry=entry,
                        date=datetime.today().date(),
                        user_id=st.session_state.user_id,
                    )
                    session.add(new_entry)
                    session.commit()
                    st.experimental_rerun()  # Rerun the app to refresh the data

    st.write("\n\n" * 11)
    st.write("-" * 777)
    if diary_updated(st.session_state.user_id):
        #
        ################## MORNING MOTIVATION
        #
        st.subheader("Daily Exercises and Pep Talks")
        col4, col5 = st.columns(2)
        with col4:
            if st.button("Morning exercise"):
                with st.spinner("Hold tight, generating your exercise..."):
                    audio_path = morning_exercise(st.session_state.user_id)
                    st.audio(audio_path)
                    with open(audio_path, "rb") as file:
                        file_bytes = file.read()

                        st.download_button(
                            label="Download",
                            data=file_bytes,
                            file_name=f"morning-exercise-{date.today().strftime('%Y-%m-%d')}.mp3",
                            mime="audio/mpeg",
                        )

            #
            ################## DAILY MOTIVATION
            #

            if st.button("Daily Motivation Pep Talk"):
                with st.spinner("Generating your daily motivation pep talk"):
                    audio_path = motivation_pep_talk(st.session_state.user_id)
                    st.audio(audio_path)
                    with open(audio_path, "rb") as file:
                        file_bytes = file.read()

                        st.download_button(
                            label="Download",
                            data=file_bytes,
                            file_name=f"pep-talk-{date.today().strftime('%Y-%m-%d')}.mp3",
                            mime="audio/mpeg",
                        )
        with col5:
            #
            ################## GET YOUR SHIT TOGETHER
            #

            if st.button("Get Your Shit Together!"):
                with st.spinner(
                    "Words of wisdom incoming, open your ears and sit up straight!"
                ):
                    audio_path = get_your_shit_together(st.session_state.user_id)
                    st.audio(audio_path)
                    with open(audio_path, "rb") as file:
                        file_bytes = file.read()

                        st.download_button(
                            label="Download",
                            data=file_bytes,
                            file_name=f"get-your-shit-together-{date.today().strftime('%Y-%m-%d')}.mp3",
                            mime="audio/mpeg",
                        )
            if st.button("Blow Your Own Trumpet"):
                with st.spinner("Are you ready to be reminded of who you really are?"):
                    audio_path = blow_your_own_trumpet(st.session_state.user_id)
                    st.audio(audio_path)
                    with open(audio_path, "rb") as file:
                        file_bytes = file.read()

                        st.download_button(
                            label="Download",
                            data=file_bytes,
                            file_name=f"blow-your-own-trumpet-{date.today().strftime('%Y-%m-%d')}.mp3",
                            mime="audio/mpeg",
                        )

    else:
        "Please make sure your gratitude diary and daily task list is up to date if you want access to the exercises and talks!"
    #
    ################## COACHING SESSIONS
    #

    st.write("\n\n" * 11)
    st.write("-" * 777)

    st.subheader("Plan Your Dreams")

    # Fetch all goals and dreams for a specific user
    with SessionLocal() as session:
        goals_and_dreams = (
            session.query(GoalsAndDreams)
            .filter_by(user_id=st.session_state.user_id)
            .all()
        )

    # Create a dictionary mapping names to ids
    dropdown_options = {gd.name: gd.id for gd in goals_and_dreams}

    # Populate dropdown in Streamlit
    selected_goal_id = st.selectbox(
        "Select a goal/dream:",
        options=list(dropdown_options.keys()),
        format_func=lambda x: x,
    )

    # Button action
    if st.button("Goal Setting Exercise"):
        # Get the id of the selected goal/dream
        goal_id = dropdown_options[selected_goal_id]
        goal_string = fetch_and_format_data(
            user_id=st.session_state.user_id,
            table=GoalsAndDreams,
            columns=["name", "description"],
            id=goal_id,
        )

        st.write(f"Your goal is: {goal_string}")

        # reset the chat whenever a new goal is selected
        st.session_state.messages = []

        system_message = f"""You are a life coach, guiding a client, {st.session_state.user_name}, through a goal-setting exercise using the SMART framework.

        The goal is:{goal_string}

        You will guide the user through each of the 5 steps separately for their goal. So first you will ask them to make their goals specific and so on.
        Once you have made the final summary of the SMART steps, don't ask any more questions """

        st.session_state.messages.append(SystemMessage(content=system_message))
        st.session_state.messages.append(HumanMessage(content="Let's get started"))

        chat = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0.7)

        response = chat(st.session_state.messages)
        st.session_state.messages.append(AIMessage(content=response.content))

    # if the chat is going on
    if "messages" in st.session_state:
        # print the latest response
        message_placeholder = st.empty()

        with st.form(key="chat", clear_on_submit=True):
            user_chat_input = st.text_area(label="Send a message")
            chat_button = st.form_submit_button(label="Chat")

        if chat_button and user_chat_input:
            # append new input, get response, append chat response
            st.session_state.messages.append(HumanMessage(content=user_chat_input))
            chat = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0.7)
            response = chat(st.session_state.messages)
            st.session_state.messages.append(AIMessage(content=response.content))

        message_placeholder.write(st.session_state.messages[-1].content)

        # Now you have both the user_id (from session_state) and goal_id
        # Run your function here
        # your_function(user_id=st.session_state.user_id, goal_id=goal_id)
