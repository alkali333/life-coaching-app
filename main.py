import streamlit as st
from datetime import datetime
from dotenv import load_dotenv, find_dotenv
import pandas as pd

# My imports
from models import GoalsAndDreams, GratitudeJournal, SessionLocal
from openai_calls import create_motivational_text
from polly import text_to_speech

# The tables we want to work with
from models import GoalsAndDreams
from db_helpers import fetch_and_format_data

load_dotenv(find_dotenv(), override=True)


st.subheader('Goals And Dreams')

# Display existing data
with SessionLocal() as session:
    existing_data = session.query(GoalsAndDreams.name, GoalsAndDreams.description).all()
    existing_data_df = pd.DataFrame(existing_data, columns=['name', 'description'])
    st.dataframe(existing_data_df)  # Use st.table if you prefer a static table

st.subheader('Add A New One')
# Form to add new entries
with st.form(key='goals_and_dreams', clear_on_submit=True):
    name = st.text_input('Name')
    description = st.text_input('Description')
    submit_button = st.form_submit_button(label='Submit')
    if submit_button:
        with SessionLocal() as session:
            new_goal = GoalsAndDreams(name=name, description=description)
            session.add(new_goal)
            session.commit()
            st.experimental_rerun()  # Rerun the app to refresh the data



# Repeat similar pattern for other tables, for example:
st.subheader('Gratitude Journal')
with st.form(key='gratitude_journal', clear_on_submit=True):
    entry = st.text_area('Entry')
    submit_button = st.form_submit_button(label='Submit')
    if submit_button:
        with SessionLocal() as session:
            new_entry = GratitudeJournal(entry=entry, date=datetime.today().date())
            session.add(new_entry)
            session.commit()

if st.button("Goals And Dreams Motivation!"):
    with st.spinner('Generating your motivation speech...'):
        user_data = fetch_and_format_data(GoalsAndDreams, columns=['name', 'description'], num_rows=None)
    
        llm_response = create_motivational_text(user_data)
        audio_path = text_to_speech(llm_response, file_name="goals_and_dreams_motivation")

        # Play the audio in the Streamlit app
        st.audio(audio_path)
        # Provide a download button for the audio file
        with open(audio_path, 'rb') as file:
            file_bytes = file.read()
            st.download_button(
                label="Download Motivation Speech",
                data=file_bytes,
                file_name="motivation-speech.mp3",
                mime="audio/mpeg"
            )

# Add similar blocks for the rest of the tables
