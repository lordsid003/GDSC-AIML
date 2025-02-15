import os
from dotenv import load_dotenv
load_dotenv()

from config import Config,prompt
from langchain_groq import ChatGroq
from langchain.memory import ConversationBufferMemory
from langchain_experimental.agents import create_csv_agent


class Model(object):
    def __init__(self) :
        self.agent = None
        self.memory = ConversationBufferMemory(return_messages=True)
        self.llm = ChatGroq(
            temperature=0, # confidence of model
            model="llama-3.3-70b-versatile",
            api_key=os.getenv("API_KEY_"),
            # api_key=st.secrets["API_KEY"]
        )
    def add_context(self,message,response):
            self.memory.save_context({"user_message": message}, {"assistant": response})
        
        
    def read_csv(self, file_path):
        self.agent = create_csv_agent(llm=self.llm,path=file_path,allow_dangerous_code=True,
                                      verbose=True,
                                      handle_parsing_errors=True)
    
    def chat(self,message:str,history=[]):
        if self.agent is None:
    
            sequence_chain = prompt | self.llm.with_structured_output(Config)
            conversation_history = self.memory.load_memory_variables({})["history"]
            full_prompt = f"{conversation_history}\nUser: {message}\nAssistant:"
            data = {"user_message":full_prompt,}

            print("chat initiated")
            response = sequence_chain.invoke(data)
            print("resp initiated")
            
            self.memory.save_context({"user_message": message}, {"assistant": response.msg})
            self.add_context(message,response.msg)
            return response.msg
        else:
            sequence_chain = prompt | self.agent 
        
            # conversation_history = self.memory.load_memory_variables({})["history"]
            full_prompt = f"{history}\nUser: {message}\nAssistant:"
            print(full_prompt)
            data = {"user_message":full_prompt,}

            print("chat initiated")
            response = sequence_chain.invoke(data)
            print("resp initiated")
            
            self.add_context(message,response["output"])

            return response["output"]
