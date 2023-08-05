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

