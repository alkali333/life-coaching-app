import os
from dotenv import load_dotenv
from sqlalchemy.orm import Session


# langchain imports
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.schema import HumanMessage, SystemMessage
from langchain.output_parsers import PydanticOutputParser

from typing import Protocol, List, Any


class ChatModel(Protocol):
    def __call__(self, messages: List[Any]) -> Any:
        ...


load_dotenv()

# test if asking with memory works if the LLM is stored in a session


class LifeCoach:
    client_name: str
    mindstate: str = "no mindstate initialised"
    query: str
    llm: ChatModel

    def __init__(self, mindstate: str, llm: ChatModel = None) -> None:
        self.mindstate = mindstate
        self.llm = llm or ChatOpenAI(
            model_name="gpt-3.5-turbo", temperature=0.7, max_tokens=1024
        )

    def create_exercise(
        self, query: str, coach_info: str = "You are a life coach"
    ) -> str:
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
        print(f"System Prompt: {formatted_message}/n/n/n")
        print(f"System Prompt: {formatted_message}/n/n/n")

        llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0.7, max_tokens=1024)

        messages = [
            SystemMessage(content=str(formatted_message)),
            HumanMessage(content=query),
        ]

        response = llm(messages)
        return response.content

    def reset_mindstate(self, new_mindstate: str):
        self.mindstate = new_mindstate
