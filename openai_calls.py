from models import GoalsAndDreams
from langchain import PromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
import re


def create_llm_content(template, user_variables=None):
    llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=1)
    if not user_variables: # if no user variables assume we are using a standard prompt
        return llm(template)
    else: # use the prompt template with the user variables
        input_variables = re.findall(r"\{(.*?)\}", template)
        if len(user_variables) != len(input_variables):
            raise ValueError("The number of user variables doesn't match the number of input variables in the prompt")
        else:
            prompt=PromptTemplate(template=template, input_variables=input_variables)        
            chain = LLMChain(llm=llm, prompt=prompt)
            return chain.run(user_variables)
