from mindstate_service import MindStateService
from models import SessionLocal
from dotenv import load_dotenv

from langchain.chat_models import ChatOpenAI
from langchain.schema import SystemMessage
from langchain.agents import OpenAIFunctionsAgent, AgentExecutor, Tool, tool


# the tool functions will have to to inside init
# the agent class will have access to a dict representing the clients
# mindstate, and a set of tools for accessing each one.
# this means the agent will be able to work with a much larger
# data set when interacting with the user, pulling in what is needed
# as necessary.


with SessionLocal() as db:
    m_s_s = MindStateService(user_id=1, db=db)


# tools can return direct! So they can break the agent loop.
@tool
def get_hopes_and_dreams() -> str:
    """Useful when looking up the clients hopes and dreams"""
    with SessionLocal() as db:
        mss = MindStateService(user_id=1, db=db)
    return mss.get_hopes_and_dreams()


@tool
def get_skills_and_achievements() -> str:
    """Useful when looking up a client's skills and achievements"""
    with SessionLocal() as db:
        mss = MindStateService(user_id=1, db=db)
    return mss.get_skills_and_achievements()


@tool
def get_obstacles_and_challenges() -> str:
    """Useful when looking up a client's obstacles and challenges"""
    with SessionLocal() as db:
        mss = MindStateService(user_id=1, db=db)
    return mss.get_obstacles_and_challenges()


@tool
def get_grateful_for() -> str:
    """Useful when looking up what the client is grateful for"""
    with SessionLocal() as db:
        mss = MindStateService(user_id=1, db=db)
    return mss.get_grateful_for()


@tool
def get_current_tasks() -> str:
    """Useful when looking up a client's current tasks"""
    with SessionLocal() as db:
        mss = MindStateService(user_id=1, db=db)
    return mss.get_current_tasks()


tools = [
    get_hopes_and_dreams,
    get_obstacles_and_challenges,
    get_skills_and_achievements,
    get_grateful_for,
    get_skills_and_achievements,
]


llm = ChatOpenAI(temperature=0)

system_message = SystemMessage(
    content="""You are a life coach. You will be asked to create exercises for the client.   \n\n
                    Always look in the info below for information when creating the exercises.
                    They can be based on their hopes and dreams, obstacles and challenges, or any other things aspects of their
                    lives as specified. 
                    Don't use numbers or headings, just prose, as if the user was listening to you speak. 
                    Around 500 words.
                    You can only create exercises if you have information about the client.
                     """
)
prompt = OpenAIFunctionsAgent.create_prompt(system_message=system_message)

agent = OpenAIFunctionsAgent(llm=llm, tools=tools, prompt=prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
agent_response = agent_executor.run(
    "Find out what the client is grateful for and create a guided visualisation exercise to reflect on these things "
)

print(agent_response)
