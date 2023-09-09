from langchain.agents import tool
from mindstate_service import MindStateService
from models import SessionLocal
from dotenv import load_dotenv

from langchain.chat_models import ChatOpenAI
from langchain.schema import SystemMessage
from langchain.agents import OpenAIFunctionsAgent, AgentExecutor, Tool


# the tool functions will have to to inside init
# the agent class will have access to a dict representing the clients
# mindstate, and a set of tools for accessing each one.
# this means the agent will be able to work with a much larger
# data set when interacting with the user, pulling in what is needed
# as necessary.


with SessionLocal() as db:
    m_s_s = MindStateService(user_id=1, db=db)

tools = [
    Tool(
        name="Get Hopes And Dreams",
        func=m_s_s.get_hopes_and_dreams(),
        description="Useful when looking up the hopes and dreams of a client",
    ),
    Tool(
        name="Get Skills And Achievements()",
        func=m_s_s.get_skills_and_achievements(),
        description="Useful when looking up the skills and achievements of a client",
    ),
    Tool(
        name="Get Obstacles And Challenges",
        func=m_s_s.get_obstacles_and_challenges(),
        description="useful for when you need to look up a client's obstacles and challenges.",
    ),
    Tool(
        name="Get Current Tasks",
        func=m_s_s.get_current_tasks(),
        description="useful for when you need to look up a client's current tasks.",
    ),
    Tool(
        name="Get Grateful fo",
        func=m_s_s.get_greatful_for(),
        description="Useful when looking up what client is grateful for",
    ),
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
agent_executor.run(
    "Find out what the client is grateful for and create a guided visualisation exercise to reflect on these things "
)
