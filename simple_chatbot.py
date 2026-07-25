from langgraph.graph import StateGraph, START, END
from langchain_core.messages import BaseMessage, HumanMessage
from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from typing import TypedDict, Annotated
from langgraph.graph.message import add_messages
from dotenv import load_dotenv
import sqlite3
import streamlit as st
import os

load_dotenv()
token = st.secrets["HUGGINGFACEHUB_API_TOKEN"]
llm = HuggingFaceEndpoint(
        repo_id="meta-llama/Llama-3.1-8B-Instruct",
        huggingfacehub_api_token=tokan
    
    )

model = ChatHuggingFace(llm=llm)


class chatstate(TypedDict):
    
    messages: Annotated[list[BaseMessage], add_messages]
    
    
def chat_node(state: chatstate):
     
    messages = state['messages']
    
    response = model.invoke(messages)
    
    return {'messages': [response]}


conn = sqlite3.connect('chatdatabase.db', check_same_thread=False)

checkpoint = SqliteSaver(conn=conn)

graph = StateGraph(chatstate)


graph.add_node('chat_node', chat_node)

graph.add_edge(START, 'chat_node')
graph.add_edge('chat_node', END)


chatbot = graph.compile(checkpointer=checkpoint)


def retrive_all_threads():
    print('checkpoint: ', checkpoint)
    all_threads = set()
    for checkpoints in checkpoint.list(None):
        all_threads.add(checkpoints.config['configurable']['thread_id'])
        
    return list(all_threads)



# initial_state = {'messages':[HumanMessage(content="what is AI")]}


# chatbot.invoke(initial_state)['messages'][-1].content


# thread_id = 1

# while True:
    
#     user_message = input('Type here: ')
#     print('user :', user_message)
    
#     if user_message.strip().lower() in ['exit', 'quit', 'bye']:
#         break
    
#     config = {'configurable': {'thread_id': '1'}}
#     response = chatbot.invoke({'messages': [HumanMessage(content=user_message)]}, config=config)
    
#     print('AI :', response['messages'][-1].content)
