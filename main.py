import streamlit as st
from datetime import datetime
from dotenv import load_dotenv, find_dotenv
from models import GoalsAndDreams, GratitudeJournal, SessionLocal
from openai_calls import motivate_hopes_and_dreams
from polly import text_to_speech

load_dotenv(find_dotenv(), override=True)


st.subheader('Goals And Dreams')
with st.form(key='goals_and_dreams', clear_on_submit=True):
    name = st.text_input('Name')
    description = st.text_input('Description')
    submit_button = st.form_submit_button(label='Submit')
    if submit_button:
        with SessionLocal() as session:
            new_goal = GoalsAndDreams(name=name, description=description)
            session.add(new_goal)
            session.commit()

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

if st.button("Motivate Me!"):
    motivation = motivate_hopes_and_dreams()
    st.write(motivation)
    audio_path = text_to_speech(motivation, file_name="motivation-speech")

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
