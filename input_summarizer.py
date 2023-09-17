from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage


# this can probably just be turned into a function
class InputSummarizer:
    def __init__(self, llm=None):
        self.llm = llm or ChatOpenAI(model="gpt-3.5-turbo", temperature="0.7")

    def summarize(self, text: str, mode="summary", user_name=""):
        if mode == "summary":
            system_message = f"""You are a life coach.{ user_name or "the client" } is going to tell you something about their life (it could be their hopes and dreams, it could be their obstacles and challenges).
                        For each issue they bring up, you are to provide a heading and a single sentance summary, number each item. Record them in a way that a life-coach working with the user would find useful.
                        If they already have headings, numbers, and single sentances, keep them the same \n\n"""
        elif mode == "spo":
            system_message = f"""You are a life coach. { user_name or "the client" }  is going to tell you something about their life (it could be their hopes and dreams, it could be their obstacles and challenges).
            convert this information to a set of SPO triples, stored as a python list. e.g.
              [["{ user_name or "client" }", "hopes to", "Building a Supportive Circle of Friends"],
              ["Building a Supportive Circle of Friends", "method", "Find and engage with like-minded individuals"]
              ["{ user_name or "client" }", "faces obstacle", "Overcoming Doubt and Procrastination"],
              ["Overcoming Doubt and Procrastination", "strategy", "Address the root cause of doubting oneself"]]
              Limit to two methods / strategies for each task identified. Remove any numbers or headings
             \n\n"""
            # system_message = "Write a 2-3 sentance summary of the provided info"
        messages = [
            SystemMessage(content=system_message),
            HumanMessage(content=text),
        ]

        return self.llm(messages)
