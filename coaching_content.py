from db_helpers import fetch_and_format_data, get_user_name
from polly import text_to_speech
from openai_calls import create_llm_content
from models import GoalsAndDreams, GratitudeJournal, CurrentProjects, PowersAndAchievements


def morning_exercise(user_id):
    template = """\
        You are a life coach, come up with a visualisation exercise for the user, {user}, to reach the following goals. Pure prose, no headings or section numbers. 
        GOALS: {goals}
    """
    user_name = get_user_name(user_id)
    goals_string = fetch_and_format_data(user_id=user_id, table=GoalsAndDreams, columns=['name', 'description'], num_rows=None)
 
    llm_response = create_llm_content(template, {"user":user_name, "goals":goals_string})

    audio_path = text_to_speech(llm_response, speed=75, voice="Emma")

    return audio_path

def get_your_shit_together(user_id):
    template = """\
        You are a strict and frightening drill drill sergeant shouting at {user}, telling them to get himself together if he wants to succeeed. Explain to them in no uncertain terms that if he doesn't carry out his responsibilities he 
        will have no hope in achieving their goals. Don't mince your words, give it to him straight! Tease them too with dry humour. Basically tell them not to be lazy and make exuses or they will end up a loser. 

        Their responsibilities are:  {currentprojects}  
        Their goals are: {goals}
    """
    user_name = get_user_name(user_id)           
    current_projects_string = fetch_and_format_data(user_id=user_id, table=CurrentProjects, columns=['entry'], num_rows=1)
    goals_string = fetch_and_format_data(user_id=user_id, table=GoalsAndDreams, columns=['name'], num_rows=None)

    llm_response = create_llm_content(template, {"user": user_name, "currentprojects": current_projects_string, "goals": goals_string})

    audio_path = text_to_speech(llm_response, speed=125, voice="Matthew")

    return audio_path

def motivation_pep_talk(user_id):
    template = """\
    Create a motivational speech/pep-talk for the user: {user}. First remind him to be grateful based on this dairy entry {gratitude}. 

    Then say something to motivate him to daily tasks from his last diary entry ( {currentprojects} ) help him imagine how it will feel to get these done, and remind him he has the skills to do it. Be very encouraging. Sign off from Emma (Your favourite AI cheer-leader)
    """

    user_name = get_user_name(user_id)    
    gratitude_string = fetch_and_format_data(user_id=user_id, table=GratitudeJournal, columns=['entry'], num_rows=1)
    current_projects_string = fetch_and_format_data(user_id=user_id, table=CurrentProjects, columns=['entry'], num_rows=1)
    
    llm_response = create_llm_content(template, {"user":user_name, "gratitude": gratitude_string, "currentprojects": current_projects_string})

    audio_path = text_to_speech(llm_response, voice="Emma")

    return audio_path