import os
from dotenv import load_dotenv
from sqlalchemy.orm import Session
import json

# langchain imports
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.schema import HumanMessage, SystemMessage
from langchain.output_parsers import PydanticOutputParser

from typing import Protocol, List, Any
from langchain.agents import OpenAIFunctionsAgent, AgentExecutor, Tool, tool


class ChatModel(Protocol):
    def __call__(self, messages: List[Any]) -> Any:
        ...


load_dotenv()


class LifeCoach:
    mindstate: str = "no mindstate initialised"
    llm: ChatModel

    def __init__(
        self,
        mindstate: str,
        coach_info: str = "You are a life coach",
        llm: ChatModel = None,
    ) -> None:
        self.mindstate = mindstate
        self.llm = llm or ChatOpenAI(
            model_name="gpt-3.5-turbo", temperature=0.7, max_tokens=1024
        )
        self.coach_info = coach_info

    def create_exercise(
        self,
        query: str,
        coach_info: str = None,
    ) -> str:
        # use default coach info if not overridden
        if not coach_info:
            coach_info = self.coach_info

        # create system prompt
        prompt = PromptTemplate(
            template="""{coach_info}. You will be asked to create exercises for the user, based only on the information provided below in JSON. Use the client name (supplied below) to personalise the exercises.  \n\n
                    Always look in the info below for information when creating the exercises. They will always be based information below in USER INFO (hopes and dreams, skills and achievements, obstacles and challenges, grateful for, or current tasks) 
                    Don't use numbers or headings, just prose, as if the user was listening to you speak. Around 500 words. You may also have conversations with the user abou these issues, using modern life-coaching techniques. 
 
                    USER INFO: {mindstate}""",
            input_variables=["coach_info", "mindstate"],
        )
        # add supplied variables
        formatted_message = prompt.format_prompt(
            coach_info=coach_info, mindstate=self.mindstate
        )

        # debugging
        print(f"Prompt sent to LLM: {formatted_message}")

        human_message = query + f" Remember {coach_info}"

        messages = [
            SystemMessage(content=str(formatted_message)),
            HumanMessage(content=human_message),
        ]

        response = self.llm(messages)
        return response.content

    def create_exercise_agent(
        self, query: str, coach_info: str = "You are a life coach"
    ) -> str:
        @tool
        def get_hopes_and_dreams() -> str:
            """Useful when looking up the clients hopes and dreams"""
            return json.loads(self.mindstate)["MindState"]["hopes and dreams"]

        @tool
        def get_skills_and_achievements() -> str:
            """Useful when looking up the clients skills and achievements"""
            return json.loads(self.mindstate)["MindState"]["skills and achievements"]

        @tool
        def get_obstacles_and_challenges() -> str:
            """Useful when looking up the clients obstacles and challenges"""
            return json.loads(self.mindstate)["MindState"]["obstacles and challenges"]

        @tool
        def get_grateful_for() -> str:
            """Useful when looking up the things the client is grateful for"""
            return json.loads(self.mindstate)["MindState"]["grateful for"]

        @tool
        def get_current_tasks() -> str:
            """Useful when looking up the clients current tasks"""
            return json.loads(self.mindstate)["MindState"]["current tasks"]

        tools = [
            get_hopes_and_dreams,
            get_skills_and_achievements,
            get_obstacles_and_challenges,
            get_grateful_for,
            get_current_tasks,
        ]

        llm = self.llm

        # With GPT 3.5, it does not always use a tool with this prompt unless you make it very
        # clear in the query, e.g. "Look up the clients obstacles and challenges then create a guided meditation"
        system_message = SystemMessage(
            content=f"""{coach_info}  You will be asked to create exercises for the client.   \n\n
                You don't know anything about the client and will need to use the tools to look up their info. 
                Don't use numbers or headings, just prose, as if the user was listening to you speak. 
                Around 500 words.
                You can only create exercises if you have information about the client.
                """
        )
        prompt = OpenAIFunctionsAgent.create_prompt(system_message=system_message)

        agent = OpenAIFunctionsAgent(llm=llm, tools=tools, prompt=prompt)
        agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
        agent_response = agent_executor.run(query)

        return agent_response

    def reset_mindstate(self, new_mindstate: str):
        self.mindstate = new_mindstate
