import os
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

from db_helpers import authenticate, retry_db_operation
from utils import extract_dictionary, display_image_if_exists
from life_coach import LifeCoach
from mindstate_service import MindStateService
from input_summarizer import InputSummarizer
from exercises import create_random_meditation
from quotes import get_random_quote

from polly import text_to_speech, text_to_speech_with_music


load_dotenv(find_dotenv(), override=True)

st.set_page_config(
    page_title="Atenshun 0.333 | Mind Makes Magic",
    page_icon=":rose:",
    layout="centered",
    initial_sidebar_state="auto",
    menu_items=None,
)


# Can set debug mode in URL or .env
if "DEBUG_MODE" not in st.session_state:
    st.session_state["DEBUG_MODE"] = os.getenv("DEBUG_MODE", "false").lower() == "true"

    params = st.experimental_get_query_params()
    if params:
        if params.get("debug", [])[0] == "true":
            st.session_state["DEBUG_MODE"] = "True"

if st.session_state["DEBUG_MODE"]:
    st.write("Debugging mode enabled")


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


def handle_login(email, password, mode):
    """This function logs the user in, initializes the mindstate, then
    initializes the LifeCoach using the selected mode then reruns the app."""

    # Open a session for the whole authentication block
    with SessionLocal() as session:
        authenticated = authenticate(session, Users, email, password)

        if authenticated:
            user_in_db = retry_db_operation(
                session,
                lambda: session.query(Users).filter_by(email=email).first(),
            )

            st.session_state.user_id = user_in_db.id
            st.session_state.user_name = user_in_db.name
            st.session_state.new_user = bool(user_in_db.is_new)

            # Make sure to use the existing session for MindStateService
            st.session_state.mindstate_service = MindStateService(
                user_id=user_in_db.id, db=session
            )
            user_mindstate = st.session_state.mindstate_service.to_json()

            # Define your coach_info dictionary here
            coach_info = {
                "Default": "You are a life coach",
                "Esoteric Alchemist": "You are a spiritual lifecoach drawing on hermeticism, western occultism, and alchemic scripture and philosopy, drawing on sources like The Kybalion, Corpus Hermetica, The Emerald Tablets, The Chymical Wedding of Christian Rosenkreutz, Atalanta Fugiens, Splendor Solis:",
                "Mountain Yogi": "You are a spiritual lifecoach drawing on concepts from ancient Yogic texts like Yoga Sutras, Bhagavad Gita, Vivekachudamani, Ashtavakra Gita, Yoga Vasistha",
                "Taoist Master": "You are a spiritual lifecoach who is a master of Taoist philosophy, drawing on texts such as Tao Te Ching, Chaung Tzu, Liezi Tzu, Hua Hu Ching, Wen-Tzu, I-Ching, Baopuzi",
                "Buddhist Monk": "You are a spiritual lifecoach who is a Buddhist monk, providing wisdom from texts like: Dhammapada, Heart Sutra, Diamond Sutra, Bodhisattvacaryāvatāra, Majjhima Nikaya",
                "Christian Crusader": "You are a Christian lifecoach, drawing on scripture and Christian theology",
                # Maybe include apologists such as St Augustine, Thomas Acquinas, Blaise Pascal, C.S Lewis, G.K Chesterton, Francis Schaeffer
                # Although perhaps better to stick to scripture.
                "Fairytale Dreamer": "You are a life-coach who is also a magic talking hamster who draws from the mystical and magical worlds of Lord of the Rings, Star Wars, Harry Potter (using characters from them to explain your points). You also draw on the author Alexandre Jardin and the Philsopher Jean Jacques Rousseau  ",
                "Kemetic Healer": "You are a Kemetic life-coach, drawing on ancient wisdom such as The Egyptian book of the dead, The Pyramid Texts, The Mxims of Ptahhotep and the work of modern Kemetic teachers like Muata Ashby, Maulana Karenga, Sharon LaBorde. For the modern works, don't mention the authors names, just their ideas. No cliches like mummies etc  ",
            }

            # get the info string for the selected mode, or None if the mode is not found
            info = coach_info[mode]
            st.session_state.life_coach = LifeCoach(user_mindstate, info)
            st.session_state.mode = mode
            st.experimental_rerun()

        else:
            st.sidebar.error("Authentication failed. Please check your credentials.")


# Define the options for the dropdown menu
options = [
    "Default",
    "Esoteric Alchemist",
    "Mountain Yogi",
    "Taoist Master",
    "Buddhist Monk",
    "Christian Crusader",
    "Fairytale Dreamer",
    "Kemetic Healer",
    # add an astrologer who uses date.today()
]

if "user_id" not in st.session_state:
    with st.sidebar.form(key="login_form"):
        email = st.text_input("Email", value="")
        password = st.text_input("Password", type="password")
        # Create the dropdown widget in the sidebar
        mode = st.selectbox("Mode", options)

        # Create a form and use the 'on_click' parameter to specify the callback function
        login_button = st.form_submit_button(label="Login")
    if login_button:
        handle_login(email, password, mode)
else:
    l, r = st.columns(2)

    with l:
        st.title("Atenshun v0.333 :black_heart: :brain: :old_key: ")
        st.write(
            f"<strong>Welcome, {st.session_state.user_name}!</strong>",
            unsafe_allow_html=True,
        )
        st.write(f"{st.session_state.quote}")

    with r:
        selected_mode = st.session_state.mode

        image_path = "./images/" + selected_mode.lower().replace(" ", "-") + ".jpg"
        if display_image_if_exists(image_path, "Mode: " + selected_mode):
            pass
        else:
            st.write(f"Mode: {selected_mode}")

    st.header("Daily Suggestions")

    if "welcome_message" not in st.session_state:
        # sets the welcome message to generic or customised depending on if the user is new
        if st.session_state.new_user:
            st.session_state.welcome_message = (
                "Welcome! Please use the form to tell me about yourself. "
            )
        else:
            #
            prompts = [
                """give the user 5 missions for today that will help them achieve their hopes and dreams, they can be small simple tasks""",
                """Recommend 3 random life-coaching exercises that will help them based on the user info """,
                """Create a short adventure story where the client is the hero, use the client info.""",
                """Give the client a total of 9 positive affirmations based on their goals / skills / obstacles""",
                """Write a humourous epic fantasy/sci-fi adventure in a world of talking animals, robots, 
                    technology and magic. Make the client the main character (pick an unusual animal with strange characteristics) is a story that has them use their skills
                    and achievements to overcome their obstacles and challenges and reach all their hopes and dreams""",
            ]
            with st.spinner("Loading your welcome message... "):
                if st.session_state.DEBUG_MODE:
                    st.session_state.welcome_message = (
                        "Debugging mode: welcome message would be here"
                    )
                else:
                    st.session_state.welcome_message = (
                        st.session_state.life_coach.create_exercise(
                            random.choice(prompts)
                        )
                    )

    st.write(st.session_state.welcome_message)

    button_placeholder = st.empty()

    # initialise current question
    if "current_question" not in st.session_state:
        if st.session_state.new_user:
            st.session_state.current_question = 1
        else:
            st.session_state.current_question = 0

    # st.write(
    #     f"debugging: current question is: {st.session_state.current_question} new user: {st.session_state.new_user}"
    # )

    if st.session_state.current_question == 0:
        st.header("Repeat Questions (optional)")
        st.write(
            """At least once a week, answer the questions again from scratch. \
            This is a powerful journaling exercise that will keep your mind focused on what \
            it needs to be focused on. As your awareness increases, your goals, skills, and challenges \
            will become clearer, the exercises will become even more powerful. """
        )
        with st.form(key="start"):
            submit_button = st.form_submit_button("Tell me about yourself")
        if submit_button:
            st.session_state.current_question = 1
            st.experimental_rerun()
    if st.session_state.current_question == 1:
        with st.form(key="hopes", clear_on_submit=True):
            st.write(
                """Tell me about some of your goals and dreams. \
                Choose 3-4, and for each one tell me why it is important, and how you will feel \
                when it is realised."""
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
                    info=response,
                    column="hopes_and_dreams",
                )
                st.session_state.current_question = 2
                st.experimental_rerun()

    elif st.session_state.current_question == 2:
        with st.form(key="skills", clear_on_submit=True):
            st.write(
                """Tell me about some of your skills and achievements. These can be talents, personality attributes,\
                  challenges you have overcome, education, work achievements or anything else.\
                  What are you good at? What are you proud of?"""
            )

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
                    info=response,
                    column="skills_and_achievements",
                )
                st.session_state.current_question = 3
                st.experimental_rerun()

    ### STEP THREE ###
    elif st.session_state.current_question == 3:
        st.write(
            """Tell me about some of the obstacles and challenges you are currently facing. \
            For each one, tell me what you think is the cause of the issue, and how you will \
            feel when it is overcome. """
        )

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
                info=response,
                column="obstacles_and_challenges",
            )
            print("Obstacles and challenges updated")
            with SessionLocal() as session:
                # Get the user instance
                user = retry_db_operation(
                    session,
                    lambda: session.query(Users)
                    .filter(Users.id == st.session_state.user_id)
                    .one(),
                )
                # reset the life coach to have the new info
                refresh_life_coach()
                print(f"Form finished, user:{user} retrieved from the database")

                if user.is_new == 1:
                    print("User is new, setting user to not new....")
                    retry_db_operation(
                        session, lambda: (setattr(user, "is_new", 0), session.commit())
                    )

                    # Fetch the user again to confirm the update
                    user_after_update = retry_db_operation(
                        session,
                        lambda: session.query(Users)
                        .filter(Users.id == st.session_state.user_id)
                        .one(),
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
            """Thanks for answering the questions. To access your meditation exercises,\
              please fill out your gratitude diary and task list. """
        )

    col3, col4 = st.columns(2)
    #
    ################## GRATITUDE JOURNAL
    if not st.session_state.new_user:
        if "gratitude_message" not in st.session_state:
            with st.spinner("Loading message... "):
                if st.session_state.DEBUG_MODE:
                    response = "Debugging mode: gratitude message would be here"
                else:
                    response = st.session_state.life_coach.create_exercise(
                        query="""
                    Write two short sentances encouraging client to write a list of five things they are grateful for (things that have recently gone well, or things they appreciate)                     
                    """
                    )
            st.session_state.gratitude_message = response

        with col3:
            st.subheader("Gratitude Journal")
            st.write(st.session_state.gratitude_message)
            with SessionLocal() as session:
                latest_entry = retry_db_operation(
                    session,
                    lambda: session.query(MindState.grateful_for)
                    .filter(MindState.user_id == st.session_state.user_id)
                    .first(),
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
        if "current_tasks_message" not in st.session_state:
            with st.spinner("Loading message... "):
                if st.session_state.DEBUG_MODE:
                    response = "Debugging mode: current missions message would be here"
                else:
                    response = st.session_state.life_coach.create_exercise(
                        query="""
                    Write two short sentances encouraging the client to write 5 tasks that can contribute towards their hopes and dreams (list them).                   
                    """
                    )
            st.session_state.current_tasks_message = response

        with col4:
            st.subheader("Current Missions")
            st.write(st.session_state.current_tasks_message)
            # Display existing data
            with SessionLocal() as session:
                current_tasks = retry_db_operation(
                    session,
                    lambda: session.query(MindState.current_tasks)
                    .filter(MindState.user_id == st.session_state.user_id)
                    .first(),
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
    ##
    # EXERCISE MAKER
    ###
    if not st.session_state.new_user:
        st.write("\n\n" * 11)
        st.write("-" * 777)

        exercise_placeholder = st.empty()

        west, east = st.columns(2)

        with west:
            st.image("./images/exercise-maker.jpg", use_column_width=True)
        with east:
            st.title("Need some suggestions?")
            st.write(
                "If you are looking for some missions to add to your list, I can suggest some for you."
            )
            if st.button("Suggest Missions"):
                query = """Please give me 7 missions for the user. These can be practical \
                        tasks or exercises like meditation and journaling. \
                        output as a python dictionary for example
                        {"Focused Breathing": "Take a deep breath and... "}
                        Only output the dictionary, no commentary or explanation"""

                with st.spinner("Suggesting some missions for you..."):
                    response = st.session_state.life_coach.create_exercise(query=query)

                # get rid of any extra stuff generated by the LLM
                # this function looks for a single dictionary with no
                # nested elements.

                missions_text = extract_dictionary(response)

                # If we have ended up with a usable dictionary string, we will build a table
                try:
                    # Convert string to dictionary
                    missions_dict = eval(missions_text)

                    # Convert dictionary to DataFrame
                    df_meditation = pd.DataFrame(
                        list(missions_dict.items()), columns=["Exercise", "Description"]
                    )

                    # Display the table in Streamlit without the index
                    exercise_placeholder.table(df_meditation.set_index("Exercise"))

                # If not, we will just display whatever the LLM returned in full
                except:
                    exercise_placeholder.write(
                        f"I apologise for any strange formatting, I sometimes find it difficult to communicate with you humans.\n\n {response}"
                    )
        # I want the response to appear here

        st.write("\n\n" * 11)
        st.write("-" * 777)

    if st.session_state.mindstate_service.was_updated_recently():
        st.title("Daily Exercises")
        st.write(
            f"Well done for keeping your gratitude journal and daily missions log up to date. You can now access the exercises!"
        )

        text_placeholder = st.empty()
        audio_placeholder = st.empty()
        download_placeholder = st.empty()

        col_left, col_center, col_right = st.columns(3)

        # Display images in columns
        with col_left:
            st.image("./images/robot-light.jpg", use_column_width=True)
            if st.button("Morning Meditation", use_container_width=True):
                query = create_random_meditation("misc")
                with st.spinner("Preparing your meditation..."):
                    response = st.session_state.life_coach.create_exercise(query=query)
                # text_placeholder.write(f"Exercise: {response}")
                with st.spinner("Nearly done... "):
                    audio_path = text_to_speech_with_music(
                        user_id=st.session_state.user_id,
                        text=response,
                        background_audio_path="./music/background.mp3",
                        speed=75,
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

        with col_center:
            st.image("./images/robot-dark.jpg", use_column_width=True)
            if st.button("Evening Meditation", use_container_width=True):
                query = create_random_meditation("any")
                with st.spinner("Preparing your meditation..."):
                    response = st.session_state.life_coach.create_exercise(query=query)
                # text_placeholder.write(f"Exercise: {response}")
                with st.spinner("Nearly done..."):
                    audio_path = text_to_speech_with_music(
                        user_id=st.session_state.user_id,
                        text=response,
                        background_audio_path="./music/background.mp3",
                        speed=75,
                        voice="Amy",
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

        with col_right:
            st.image("./images/robot-megaphone.jpg", use_column_width=True)
            if st.button("No Nonsense Pep Talk", use_container_width=True):
                coach_info = """You are hard-hitting, no nonsense drill sergeant, like the one out of full metal jacket, very strict, you don't mince your words!
                                You don't want your solider to end up as a pathetic loser, you are going to shout at them until they get their act together! 
                                You will be asked to create exercises for the user, based only on the information provided below in JSON. Use their name in the exercises. """

                query = """Create a motivational talk for the user, explaining them how important it is to get their current tasks done. Point out to them that the tasks
                    are essential if they are going to fulfill their hopes and dreams """

                with st.spinner("Preparing your pep talk..."):
                    response = st.session_state.life_coach.create_exercise(
                        coach_info=coach_info, query=query
                    )
                # text_placeholder.write(f"Exercise: {response}")
                with st.spinner("Shut up and wait..."):
                    audio_path = text_to_speech(
                        user_id=st.session_state.user_id,
                        text=response,
                        speed=110,
                        voice="Matthew",
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

        text_placeholder = st.empty()
        audio_placeholder = st.empty()
        download_placeholder = st.empty()

        # col5, col6, col7 = st.columns(3)
        # with col5:
        #     if st.button("Random Exercise"):
        #         query = create_random_meditation("misc")
        #         response = st.session_state.life_coach.create_exercise(query=query)
        #         # text_placeholder.write(f"Exercise: {response}")
        #         audio_path = text_to_speech_with_music(
        #             user_id=st.session_state.user_id,
        #             text=response,
        #             background_audio_path="./music/background.mp3",
        #             speed=75,
        #         )
        #         audio_placeholder.audio(audio_path)
        #         with open(audio_path, "rb") as file:
        #             file_bytes = file.read()

        #         download_placeholder.download_button(
        #             label="Download",
        #             data=file_bytes,
        #             file_name=f"random-{date.today().strftime('%Y-%m-%d')}.mp3",
        #             mime="audio/mpeg",
        #         )
        # with col6:
        #     if st.button("No Nonsense Pep Talk"):
        #         coach_info = """You are hard-hitting, no nonsense drill sergeant, like the one out of full metal jacket, very strict, you don't mince your words!
        #                         You don't want your solider to end up as a pathetic loser, you are going to shout at them until they get their act together!
        #                         You will be asked to create exercises for the user, based only on the information provided below in JSON. Use their name in the exercises. """

        #         query = """Create a motivational talk for the user, explaining them how important it is to get their current tasks done. Point out to them that the tasks
        #             are essential if they are going to fulfill their hopes and dreams """

        #         response = st.session_state.life_coach.create_exercise(
        #             coach_info=coach_info, query=query
        #         )
        #         # text_placeholder.write(f"Exercise: {response}")
        #         audio_path = text_to_speech(
        #             user_id=st.session_state.user_id,
        #             text=response,
        #             speed=110,
        #             voice="Matthew",
        #         )
        #         audio_placeholder.audio(audio_path)
        #         with open(audio_path, "rb") as file:
        #             file_bytes = file.read()

        #         download_placeholder.download_button(
        #             label="Download",
        #             data=file_bytes,
        #             file_name=f"random-{date.today().strftime('%Y-%m-%d')}.mp3",
        #             mime="audio/mpeg",
        #         )
        # with col7:
        #     if st.button("Manifest Your Dreams"):
        #         query = create_random_meditation("hopes_and_dreams")

        #         response = st.session_state.life_coach.create_exercise(query=query)
        #         # text_placeholder.write(f"Exercise: {response}")
        #         audio_path = text_to_speech(
        #             user_id=st.session_state.user_id, text=response, speed=75
        #         )
        #         audio_placeholder.audio(audio_path)
        #         with open(audio_path, "rb") as file:
        #             file_bytes = file.read()

        #         download_placeholder.download_button(
        #             label="Download",
        #             data=file_bytes,
        #             file_name=f"random-{date.today().strftime('%Y-%m-%d')}.mp3",
        #             mime="audio/mpeg",
        #         )
        # col9, col10, col11 = st.columns(3)
        # with col9:
        #     if st.button("Boost your self-esteem"):
        #         query = create_random_meditation("skills_and_achievements")

        #         response = st.session_state.life_coach.create_exercise(query=query)
        #         # text_placeholder.write(f"Exercise: {response}")
        #         audio_path = text_to_speech(
        #             user_id=st.session_state.user_id, text=response, speed=75
        #         )
        #         audio_placeholder.audio(audio_path)
        #         with open(audio_path, "rb") as file:
        #             file_bytes = file.read()

        #         download_placeholder.download_button(
        #             label="Download",
        #             data=file_bytes,
        #             file_name=f"random-{date.today().strftime('%Y-%m-%d')}.mp3",
        #             mime="audio/mpeg",
        #         )
        # with col10:
        #     if st.button("Self-EMPOWERMENT!"):
        #         query = create_random_meditation("empowerment")

        #         response = st.session_state.life_coach.create_exercise(query=query)
        #         # text_placeholder.write(f"Exercise: {response}")
        #         audio_path = text_to_speech(
        #             user_id=st.session_state.user_id, text=response, speed=75
        #         )
        #         audio_placeholder.audio(audio_path)
        #         with open(audio_path, "rb") as file:
        #             file_bytes = file.read()

        #         download_placeholder.download_button(
        #             label="Download",
        #             data=file_bytes,
        #             file_name=f"random-{date.today().strftime('%Y-%m-%d')}.mp3",
        #             mime="audio/mpeg",
        #         )
        # with col11:
        #     if st.button("Get things done!"):
        #         query = create_random_meditation("current_tasks")

        #         response = st.session_state.life_coach.create_exercise(query=query)
        #         # text_placeholder.write(f"Exercise: {response}")
        #         audio_path = text_to_speech(
        #             user_id=st.session_state.user_id, text=response, voice="Matthew"
        #         )
        #         audio_placeholder.audio(audio_path)
        #         with open(audio_path, "rb") as file:
        #             file_bytes = file.read()

        #         download_placeholder.download_button(
        #             label="Download",
        #             data=file_bytes,
        #             file_name=f"random-{date.today().strftime('%Y-%m-%d')}.mp3",
        #             mime="audio/mpeg",
        #         )

        ######## Custom Exercise
        #
        if not st.session_state.new_user:
            st.write("\n\n" * 11)
            st.write("-" * 777)

            st.subheader("Create your own exercise")
            with st.form(key="custom_exercise", clear_on_submit=True):
                custom_text = st.text_area(
                    "Tell me a goal, a challenge, or something you would like to work on and I will make a custom exercise for you"
                )
                custom_button = st.form_submit_button("Create!")
            if custom_button:
                query = custom_text
                with st.spinner("Creating your custom exercise... "):
                    custom_response = st.session_state.life_coach.create_exercise(
                        query=custom_text
                    )
                with st.spinner("Nearly done... "):
                    audio_path = text_to_speech_with_music(
                        user_id=st.session_state.user_id,
                        text=custom_response,
                        background_audio_path="./music/background.mp3",
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
        # Maybe no need for this in the app

        # st.write("\n\n" * 11)
        # st.write("-" * 777)

        # st.subheader("Plan Your Dreams")

        # st.write("Goal Setting Exercise")

        # if "messages" not in st.session_state:
        #     with st.form(key="goal_setting", clear_on_submit=True):
        #         goal_string = st.text_area(
        #             "Enter a goal to get started. Use as much detail as you like."
        #         )
        #         goal_button = st.form_submit_button("Guide me to my goal!")
        # if goal_button:
        #     st.session_state.messages = []

        #     system_message = f"""You are a life coach, guiding a client, {st.session_state.user_name}, through a goal-setting exercise using the SMART framework.

        #         The goal is:{goal_string}

        #         You will guide the user through each of the 5 steps separately for their goal. So first you will ask them to make their goals specific and so on.
        #         Once you have made the final summary of the SMART steps, don't ask any more questions but provide a lists of tasks for the user based on their responses and your insights """

        #     st.session_state.messages.append(SystemMessage(content=system_message))
        #     st.session_state.messages.append(HumanMessage(content="Let's get started"))

        #     chat = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0.7)

        #     response = chat(st.session_state.messages)
        #     st.session_state.messages.append(AIMessage(content=response.content))

        # # if the chat is going on
        # if "messages" in st.session_state:
        #     # print the latest response
        #     message_placeholder = st.empty()
        #     audio_placeholder = st.empty()

        #     with st.form(key="chat", clear_on_submit=True):
        #         user_chat_input = st.text_area(label="Send a message")
        #         chat_button = st.form_submit_button(label="Chat")

        #     if chat_button and user_chat_input:
        #         # append new input, get response, append chat response
        #         st.session_state.messages.append(HumanMessage(content=user_chat_input))
        #         chat = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0.7)
        #         response = chat(st.session_state.messages)
        #         st.session_state.messages.append(AIMessage(content=response.content))

        #     final_message = st.session_state.messages[-1].content
        #     if len(st.session_state.messages) == 13:
        #         final_message = (
        #             final_message
        #             + """ . Remember, you can add this list of suggestions to
        #             your current task diary above. Keep your diaries updated to access these coaching exercises."""
        #         )

        #     st.write(f"MESSAGE COUNTER: {len(st.session_state.messages)}")
        #     message_placeholder.write(final_message)

        #     audio_path = text_to_speech(
        #         user_id=st.session_state.user_id, text=final_message
        #     )

        #     # Open the audio file using the returned path and play it in the placeholder
        #     with open(audio_path, "rb") as audio_file:
        #         audio_bytes = audio_file.read()
        #         audio_placeholder.audio(audio_bytes, format="audio/mp3")

    else:
        "Please make sure your gratitude diary and daily task list is up to date if you want access to the exercises and talks!"

    #
    ######## Dairy
    #
    if not st.session_state.new_user:
        st.write("\n\n" * 11)
        st.write("-" * 777)

        left, right = st.columns(2)

        diary_audio_placeholder = st.empty()

        with left:
            st.image(image="./images/robot-diary.jpg")
        with right:
            st.write(
                """This is your diary, use it to keep track of your progress. What has gone well lately? What has been challenging?
            Enter your diary and I will analyse it for you."""
            )
            with st.form(key="diary", clear_on_submit=True):
                diary_entry = st.text_area("Entry")
                diary_submit_button = st.form_submit_button(label="Enter")

                if diary_submit_button:
                    input_summarizer = InputSummarizer()
                    with st.spinner("Reading your diary..."):
                        summary = input_summarizer.summarize(
                            text=diary_entry,
                            mode="diary",
                            user_name=st.session_state.user_name,
                        )
                    with SessionLocal() as session:
                        new_entry = Diary(
                            entry=diary_entry,
                            summary=summary,
                            date=datetime.today().date(),
                            user_id=st.session_state.user_id,
                        )
                        retry_db_operation(session, session.add, new_entry)

                    st.write("Diary Updated!")
                    with st.spinner("Analysing your diary..."):
                        coach_response = st.session_state.life_coach.create_exercise(
                            query=f"""Give your analysis of this diary entry with regard to the 
                                    info you have about this client, make suggestions. Address the client directly,
                                    don't sign off with "your name" or anything else. 
                                    "You are... " Diary Entry:{summary}"""
                        )
                        # st.write(coach_response)

                        audio_path = text_to_speech(
                            user_id=st.session_state.user_id, text=coach_response
                        )

                    with open(audio_path, "rb") as audio_file:
                        audio_bytes = audio_file.read()
                        diary_audio_placeholder.audio(audio_bytes, format="audio/mp3")
