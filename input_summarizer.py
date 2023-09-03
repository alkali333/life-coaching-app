from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage


class InputSummarizer:
    def __init__(self, model="gpt-3.5-turbo", temperature="0.7"):
        self.llm = ChatOpenAI(model=model, temperature=temperature)

    def summarize(self, text: str):
        system_message = """You are a life coach. The user is going to tell you something about their life (it could be their hopes and dreams, it could be their obstacles and challenges).
                    For each issue they bring up, you are to provide a heading and a single sentance summary, number each item.
                     If they already have headings, numbers keep them the same \n\n"""
        messages = [
            SystemMessage(content=system_message),
            HumanMessage(content=text),
        ]

        return self.llm(messages)
