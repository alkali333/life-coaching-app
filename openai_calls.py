from models import GoalsAndDreams, SessionLocal
from langchain import PromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain



def create_motivational_text(user_info):
    prompt_template = """\
    You are a life coach, come up with a visualisation exercise to the user reach the following goals. Pure prose, no headings or section numbers. 
    {goals}
    """

    prompt = PromptTemplate(
    template=prompt_template, input_variables=["goals"]
    )
    
    llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=1)
    
    chain = LLMChain(llm=llm, prompt=prompt)
    return chain.run(user_info)


def create_daily_motivational_text(last_gratitude_string, last_current_task_string):
    prompt_template = """\
Create a motivational pep-talk for the user Jake. First remind him to be grateful based on this dairy entry {gratitude}. 

Then say something to motivate him to daily tasks from his last diary entry ( {dailytasks} ) help him imagine how it will feel to get these done, and remind him he has the skills to do it. Be very encouraging. Sign it from Emma (Your favourite AI cheer-leader)
    """

    prompt = PromptTemplate(
    template=prompt_template, input_variables=["gratitude", "dailytasks"]
    )
    
    llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=1)
    
    chain = LLMChain(llm=llm, prompt=prompt)
    return chain.run({"gratitude": last_gratitude_string, "dailytasks": last_current_task_string})

