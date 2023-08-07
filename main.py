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
from openai_calls import create_motivational_text, create_daily_motivational_text, create_harsh_pep_talk
from polly import text_to_speech

# The tables we want to work with
from db_helpers import fetch_and_format_data, diary_updated

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
################## GRATITUDE JOURNAL 
#

    st.subheader('Gratitude Journal')
    # Display existing data
    with SessionLocal() as session:
        existing_data = session.query(GratitudeJournal.date, GratitudeJournal.entry)\
                            .filter(GratitudeJournal.user_id == st.session_state.user_id)\
                            .order_by(desc(GratitudeJournal.date))\
                            .limit(5)\
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
                        .limit(5)\
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

        st.subheader('Daily Exercise')
        if st.button("Goals And Dreams Visualisation!"):
            with st.spinner('Generating your daily exercise...'):
                user_data = fetch_and_format_data(GoalsAndDreams, columns=['name', 'description'], num_rows=None)
            
                llm_response = create_motivational_text(user=st.session_state.user_name, user_data=user_data)

                # generate audio
                audio_path = text_to_speech(llm_response, file_name="goals_and_dreams_motivation", speed=75, voice="Emma")

                # Play the audio in the Streamlit app
                st.audio(audio_path)
                # Provide a download button for the audio file
                with open(audio_path, 'rb') as file:
                    file_bytes = file.read()
                    st.download_button(
                        label="Download Goals And Dreams Visualisation",
                        data=file_bytes,
                        file_name="motivation-speech.mp3",
                        mime="audio/mpeg"
                    )

    #
    ################## DAILY MOTIVATION
    #

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
                audio_path = text_to_speech(llm_response, file_name=file_name, voice="Emma")

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
    #
    ################## GET YOUR SHIT TOGETHER
    #

        if st.button("Get Your Shit Together!"):
            with st.spinner("Words of wisdom incoming, open your ears and sit up straight!"):
                hopes_and_dreams_string = fetch_and_format_data(GoalsAndDreams, columns=['name'], num_rows=None)
                goals_string = fetch_and_format_data(CurrentProjects, columns=['entry'], num_rows=1)
                llm_response= create_harsh_pep_talk(
                                user=st.session_state.user_name, 
                                hopes_and_dreams_string=hopes_and_dreams_string, 
                                goals_string=goals_string
                                )
                
                file_name = "harsh_pep_talk"
                # generate audio
                audio_path = text_to_speech(llm_response, file_name=file_name, speed=125, voice="Matthew")

                # Play the audio in the Streamlit app
                st.audio(audio_path)
                # # Provide a download button for the audio file
                with open(audio_path, 'rb') as file:
                    file_bytes = file.read()
                    st.download_button(
                        label="Download Pep Talk",
                        data=file_bytes,
                        file_name=file_name +".mp3",
                        mime="audio/mpeg"
                    )

    else:
        "Please make sure your gratitude diary and daily task list is up to date if you want access to the exercises and talks!"
##### Implement a pep talk that takes the names of the goals and dreams as well as the daily tasks and links them
            