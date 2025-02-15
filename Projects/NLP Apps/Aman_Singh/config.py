from langchain_core.prompts import PromptTemplate
from pydantic import BaseModel,Field

class Config(BaseModel):
    msg: str = Field("")

prompt = PromptTemplate(
input_variables=["user_message"],
template=
"""
    You are A Finance Manager. 
    You need to behave and respond likely
    User says: {user_message}
""",
validate_template=True
    
)

    
