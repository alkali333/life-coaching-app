from models import GoalsAndDreams, SessionLocal
from langchain import PromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain



def motivate_hopes_and_dreams():
    # Create a session for the database
    db_session = SessionLocal()

    # Query all the Goals and Dreams
    goals_and_dreams = db_session.query(GoalsAndDreams).all()

    # Format the Goals and Dreams into the desired string
    formatted_string = ', '.join([f'{goal.name}: {goal.description}' for goal in goals_and_dreams])

    # Close the database session
    db_session.close()

    prompt_template = """\
    You are a life coach, come up with a visualisation exercise to the user reach the following goals
    {goals}
    """

    prompt = PromptTemplate(
    template=prompt_template, input_variables=["goals"]
    )
    
    llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=1)
    
    chain = LLMChain(llm=llm, prompt=prompt)
    return chain.run(formatted_string)

