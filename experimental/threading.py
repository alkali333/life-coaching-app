import threading
import streamlit as st

# Your existing text_to_speech_with_music function


def run_in_thread(fn, *args, **kwargs):
    thread = threading.Thread(target=fn, args=args, kwargs=kwargs)
    thread.start()
    return thread


# A placeholder to provide feedback to the user
def set_audio_placeholder(placeholder, default_message="Processing... Please wait."):
    placeholder.empty()
    placeholder.info(default_message)


# Streamlit code where you call the text_to_speech function
if (
    "audio_thread" not in st.session_state
    or not st.session_state.audio_thread.is_alive()
):
    # Start the thread and save it in session state
    st.session_state.audio_thread = run_in_thread(
        text_to_speech_with_music,
        user_id=st.session_state.user_id,
        text=custom_response,
        background_audio_path="./music/background.mp3",
    )

    # Set a placeholder message to let the user know the task is running
    audio_placeholder = st.empty()
    set_audio_placeholder(audio_placeholder)

    # You can later check if the thread is done and display the result
    # For example, you could use a button to refresh the status
    if st.button("Check if audio is ready"):
        if not st.session_state.audio_thread.is_alive():
            # Once the thread is done, you can display the audio
            # Assuming the audio file path is known and is the same as the one being processed
            audio_path = f"user_audio/{st.session_state.user_id}/final_output.mp3"
            with open(audio_path, "rb") as file:
                file_bytes = file.read()
                audio_placeholder.audio(file_bytes)
        else:
            set_audio_placeholder(
                audio_placeholder, "Still processing... Please wait a bit longer."
            )
else:
    set_audio_placeholder(
        audio_placeholder, "A task is currently running... Please wait."
    )
