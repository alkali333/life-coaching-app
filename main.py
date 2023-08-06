import streamlit as st

import streamlit_authenticator as stauth
from werkzeug.security import check_password_hash
import bcrypt
import yaml

from datetime import datetime
from dotenv import load_dotenv, find_dotenv
import pandas as pd
from sqlalchemy import desc

# My imports
from models import GoalsAndDreams, GratitudeJournal, CurrentProjects, Users, SessionLocal
from openai_calls import create_motivational_text, create_daily_motivational_text
from polly import text_to_speech

# The tables we want to work with
from db_helpers import fetch_and_format_data

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
    email = st.sidebar.text_input("Email")
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
    # ... Rest of your Streamlit app content for authenticated users ...


    st.subheader('Goals And Dreams')

    # Display existing data
    with SessionLocal() as session:
        existing_data = session.query(GoalsAndDreams.name, GoalsAndDreams.description)\
                            .filter(GoalsAndDreams.user_id == st.session_state.user_id)\
                            .all()
        existing_data_df = pd.DataFrame(existing_data, columns=['name', 'description'])
        st.dataframe(existing_data_df)  # Use st.table if you prefer a static table

    # Form to add new entries
    with st.form(key='goals_and_dreams', clear_on_submit=True):
        name = st.text_input('Name')
        description = st.text_input('Description')
        submit_button = st.form_submit_button(label='Submit')
        if submit_button:
            with SessionLocal() as session:
                new_goal = GoalsAndDreams(name=name, description=description, user_id=st.session_state.user_id  )
                session.add(new_goal)
                session.commit()
                st.experimental_rerun()  # Rerun the app to refresh the data

    st.subheader('Gratitude Journal')
    # Display existing data
    with SessionLocal() as session:
        existing_data = session.query(GratitudeJournal.date, GratitudeJournal.entry)\
                            .filter(GratitudeJournal.user_id == st.session_state.user_id)\
                            .order_by(desc(GratitudeJournal.date))\
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

    st.subheader('Current Tasks')
    # Display existing data
    with SessionLocal() as session:
        existing_data = session.query(CurrentProjects.date, CurrentProjects.entry)\
                        .filter(CurrentProjects.user_id == st.session_state.user_id)\
                        .order_by(desc(CurrentProjects.date))\
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


    st.subheader('Morning Motivation')
    if st.button("Goals And Dreams Motivation!"):
        with st.spinner('Generating your daily exercise...'):
            user_data = fetch_and_format_data(GoalsAndDreams, columns=['name', 'description'], num_rows=None)
        
            llm_response = create_motivational_text(user=st.session_state.user_name, user_data=user_data)

            # generate audio
            audio_path = text_to_speech(llm_response, file_name="goals_and_dreams_motivation", speed=75)

            # Play the audio in the Streamlit app
            st.audio(audio_path)
            # Provide a download button for the audio file
            with open(audio_path, 'rb') as file:
                file_bytes = file.read()
                st.download_button(
                    label="Download Daily Exercise",
                    data=file_bytes,
                    file_name="motivation-speech.mp3",
                    mime="audio/mpeg"
                )

    if st.button("Daily Motivation"):
        with st.spinner("Generating your daily motivation pep talk"):
            last_gratitude_string = fetch_and_format_data(GratitudeJournal, columns=['entry'], num_rows=1)
            last_current_task_string = fetch_and_format_data(CurrentProjects, columns=['entry'], num_rows=1)

            llm_response = create_daily_motivational_text(
                user=st.session_state.user_name, 
                last_gratitude_string=last_gratitude_string, 
                last_current_task_string=last_current_task_string)

            file_name = "daily_motivation"
            # generate audio
            audio_path = text_to_speech(llm_response, file_name=file_name)

            # Play the audio in the Streamlit app
            st.audio(audio_path)
            # # Provide a download button for the audio file
            with open(audio_path, 'rb') as file:
                file_bytes = file.read()
                st.download_button(
                    label="Download Daily Motivation Speech",
                    data=file_bytes,
                    file_name=file_name +".mp3",
                    mime="audio/mpeg"
                )

    # if st.button("Get Your Shit Together!"):
    #     with st.spinner("Words of wisdom incoming, open your ears and sit up straight!"):
    #         hopes_and_dreams_string = fetch_and_format_data(GoalsAndDreams, columns=['name'], num_rows=None)
    #         goals_string = fetch_and_format_data(CurrentProjects, columns=['entry'], num_rows=1)
    


##### Implement a pep talk that takes the names of the goals and dreams as well as the daily tasks and links them
            