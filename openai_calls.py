from models import GoalsAndDreams, SessionLocal
from langchain import PromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain



def create_motivational_text(user, user_data):
    prompt_template = f"""\
    You are a life coach, come up with a visualisation exercise for the user, {user}, to reach the following goals. Pure prose, no headings or section numbers. 
    {{goals}}
    """

    prompt = PromptTemplate(
    template=prompt_template, input_variables=["goals"]
    )
    
    llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=1)
    
    chain = LLMChain(llm=llm, prompt=prompt)
    return chain.run(user_data)


def create_daily_motivational_text(user, last_gratitude_string, last_current_task_string):
    prompt_template = f"""\
    Create a motivational speech/pep-talk for the user {user}. First remind him to be grateful based on this dairy entry {{gratitude}}. 

    Then say something to motivate him to daily tasks from his last diary entry ( {{dailytasks}} ) help him imagine how it will feel to get these done, and remind him he has the skills to do it. Be very encouraging. Sign off from Emma (Your favourite AI cheer-leader)
    """

    prompt = PromptTemplate(
    template=prompt_template, input_variables=["gratitude", "dailytasks"]
    )
    
    llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=1)
    
    chain = LLMChain(llm=llm, prompt=prompt)
    return chain.run({"gratitude": last_gratitude_string, "dailytasks": last_current_task_string})

def create_harsh_pep_talk(user, hopes_and_dreams_string, goals_string):
    prompt_template = f"""\
    You are a strict and frightening drill drill sergeant shouting at {user}, telling him to get himself together if he wants to succeeed. Explain to him that if he doesn't carry out his responsibilities he 
     will have no hope in achieving his goals. Don't mince your words, give it to him straight! Tease him too with dry humour.

    His responsibilities are:  {{currentprojects}}  
    His goals are: {{goals}}
"""

    prompt = PromptTemplate(
    template=prompt_template, input_variables=["currentprojects", "goals"]
    )
    
    llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=1)
    
    chain = LLMChain(llm=llm, prompt=prompt)
    return chain.run({"goals": hopes_and_dreams_string, "currentprojects": goals_string})


