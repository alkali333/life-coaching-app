import streamlit as st

import streamlit_authenticator as stauth
from werkzeug.security import check_password_hash
import yaml

from datetime import date, datetime
from dotenv import load_dotenv, find_dotenv
import pandas as pd
from sqlalchemy import desc

# My imports
from models import GoalsAndDreams, GratitudeJournal, CurrentProjects, Users, PowersAndAchievements, SessionLocal
from coaching_content import morning_exercise, motivation_pep_talk, get_your_shit_together

# The tables we want to work with
from db_helpers import diary_updated

load_dotenv(find_dotenv(), override=True)


# Authenticating user with Streamlit-Authenticator
def authenticate(email, password):
    with open('users.yaml', 'r') as file:
        users = yaml.safe_load(file)

    for user in users:
        if user['email'] == email and check_password_hash(user['password'], password):
            return True
    return False



if 'user_id' not in st.session_state:
    email = st.sidebar.text_input("Email", value="jake@alkalimedia.co.uk")
    password = st.sidebar.text_input("Password", type="password")
    
    if st.sidebar.button("Login"):
        if authenticate(email, password):
            with SessionLocal() as session:
                user_in_db = session.query(Users).filter_by(email=email).first()
                if user_in_db:
                    st.session_state.user_id = user_in_db.id
                    st.session_state.user_name = user_in_db.name  # Storing the user's name in session state
                else:
                    st.sidebar.text("User email not found in database.")
        else:
            st.sidebar.text("Authentication failed. Please check your credentials.")
else:
    st.write(f"Welcome, {st.session_state.user_name}!")  # Greeting the user by their name



#
################## GOALS AND DREAMS
#

    st.subheader('Goals And Dreams')

    # Display existing data
    with SessionLocal() as session:
        existing_data = session.query(GoalsAndDreams.name, GoalsAndDreams.description)\
                            .filter(GoalsAndDreams.user_id == st.session_state.user_id)\
                            .all()
        existing_data_df = pd.DataFrame(existing_data, columns=['name', 'description'])
        st.table(existing_data_df)

    # Count the number of existing entries
    count_records = len(existing_data)

    # Display form for new entry if less than 3 entries exist
    if count_records < 3:
        with st.form(key='goals_and_dreams', clear_on_submit=True):
            name = st.text_input('Name')
            description = st.text_input('Description')
            submit_button = st.form_submit_button(label='Submit')

            if submit_button:
                with SessionLocal() as session:
                    new_goal = GoalsAndDreams(name=name, description=description, user_id=st.session_state.user_id)
                    session.add(new_goal)
                    session.commit()
                    st.experimental_rerun()  # Rerun the app to refresh the data
    else:
        st.write("You've reached the limit of 3 entries.")

    if st.button("Clear All Entries"):
        with SessionLocal() as session:
            session.query(GoalsAndDreams).filter(GoalsAndDreams.user_id == st.session_state.user_id).delete()
            session.commit()
            st.experimental_rerun()  # Rerun the app to refresh the data

#
################## POWERS AND ACHIEVEMENTS
#

    st.subheader('Powers And Achievements')

    # Display existing data
    with SessionLocal() as session:
        existing_data = session.query(PowersAndAchievements.name, PowersAndAchievements.description)\
                            .filter(PowersAndAchievements.user_id == st.session_state.user_id)\
                            .all()
        existing_data_df = pd.DataFrame(existing_data, columns=['name', 'description'])
        st.table(existing_data_df)

    # Count the number of existing entries
    count_records = len(existing_data)

    # Display form for new entry if less than 3 entries exist
    if count_records < 5:
        with st.form(key='powers_and_achievements', clear_on_submit=True):
            name = st.text_input('Name')
            description = st.text_input('Description')
            submit_button = st.form_submit_button(label='Submit')

            if submit_button:
                with SessionLocal() as session:
                    new_goal = PowersAndAchievements(name=name, description=description, user_id=st.session_state.user_id)
                    session.add(new_goal)
                    session.commit()
                    st.experimental_rerun()  # Rerun the app to refresh the data
    else:
        st.write("You've reached the limit of 5 entries.")

    if st.button("Clear All Entries", key="clear_all_powers"):
        with SessionLocal() as session:
            session.query(PowersAndAchievements).filter(PowersAndAchievements.user_id == st.session_state.user_id).delete()
            session.commit()
            st.experimental_rerun()  # Rerun the app to refresh the data

#
################## GRATITUDE JOURNAL 
#

    st.subheader('Gratitude Journal')
    # Display existing data
    with SessionLocal() as session:
        existing_data = session.query(GratitudeJournal.date, GratitudeJournal.entry)\
                            .filter(GratitudeJournal.user_id == st.session_state.user_id)\
                            .order_by(desc(GratitudeJournal.date))\
                            .limit(3)\
                            .all()
        existing_data_df = pd.DataFrame(existing_data, columns=['date', 'entry'])
        st.dataframe(existing_data_df)

    # Form to add new entries
    with st.form(key='gratitude_journal', clear_on_submit=True):
        entry = st.text_area('Entry')
        submit_button = st.form_submit_button(label='Submit')
        if submit_button:
            with SessionLocal() as session:
                new_entry = GratitudeJournal(entry=entry, date=datetime.today().date(), user_id=st.session_state.user_id )
                session.add(new_entry)
                session.commit()
                st.experimental_rerun()  # Rerun the app to refresh the data

#
################## CURRENT TASKS
#

    st.subheader('Current Tasks')
    # Display existing data
    with SessionLocal() as session:
        existing_data = session.query(CurrentProjects.date, CurrentProjects.entry)\
                        .filter(CurrentProjects.user_id == st.session_state.user_id)\
                        .order_by(desc(CurrentProjects.date))\
                        .limit(3)\
                        .all()
        existing_data_df = pd.DataFrame(existing_data, columns=['date', 'entry'] )
        st.dataframe(existing_data_df)

    # Form to add new entries
    with st.form(key='current_tasks', clear_on_submit=True):
        entry = st.text_area('Entry')
        submit_button = st.form_submit_button(label='Submit')
        if submit_button:
            with SessionLocal() as session:
                new_entry = CurrentProjects(entry=entry, date=datetime.today().date(), user_id=st.session_state.user_id)
                session.add(new_entry)
                session.commit()
                st.experimental_rerun()  # Rerun the app to refresh the data


    if diary_updated(st.session_state.user_id):

    #
    ################## MORNING MOTIVATION
    #

        st.subheader('Daily Exercises and Pep Talks')
        if st.button("Morning exercise"):
            with st.spinner('Hold tight, generating your exercise...'):            
                audio_path = morning_exercise(st.session_state.user_id)
                st.audio(audio_path)
                with open(audio_path, 'rb') as file:
                    file_bytes = file.read()

                    st.download_button(
                        label="Download",
                        data=file_bytes,
                        file_name=f"morning-exercise-{date.today().strftime('%Y-%m-%d')}.mp3",
                        mime="audio/mpeg"
                    )


    #
    ################## DAILY MOTIVATION
    #

        if st.button("Daily Motivation Pep Talk"):
            with st.spinner("Generating your daily motivation pep talk"):
                audio_path = motivation_pep_talk(st.session_state.user_id)
                st.audio(audio_path)
                with open(audio_path, 'rb') as file:
                    file_bytes = file.read()

                    st.download_button(
                        label="Download",
                        data=file_bytes,
                        file_name=f"pep-talk-{date.today().strftime('%Y-%m-%d')}.mp3",
                        mime="audio/mpeg"
                    )

    #
    ################## GET YOUR SHIT TOGETHER
    #

        if st.button("Get Your Shit Together!"):
            with st.spinner("Words of wisdom incoming, open your ears and sit up straight!"):
                audio_path = get_your_shit_together(st.session_state.user_id)
                st.audio(audio_path)
                with open(audio_path, 'rb') as file:
                    file_bytes = file.read()

                    st.download_button(
                        label="Download",
                        data=file_bytes,
                        file_name=f"get-your-shit-together-{date.today().strftime('%Y-%m-%d')}.mp3",
                        mime="audio/mpeg"
                    )

    else:
        "Please make sure your gratitude diary and daily task list is up to date if you want access to the exercises and talks!"

            