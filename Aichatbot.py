import streamlit as st
from langchain_huggingface import HuggingFaceEndpoint, ChatHuggingFace
from langchain_core.messages import HumanMessage, AIMessage
import os
    
    
    
token = st.secrets["HUGGINGFACEHUB_API_TOKEN"]
# Load model only once
@st.cache_resource
def load_model():

    llm = HuggingFaceEndpoint(
        repo_id="meta-llama/Llama-3.1-8B-Instruct",
        huggingfacehub_api_token=token,
        temperature=0.2,
        max_new_tokens=500
    )

    return ChatHuggingFace(llm=llm)

model = load_model()

st.title("AI Assistant")

# Chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Display previous messages
for msg in st.session_state.chat_history:

    if isinstance(msg, HumanMessage):
        with st.chat_message("user"):
            st.write(msg.content)

    elif isinstance(msg, AIMessage):
        with st.chat_message("assistant"):
            st.write(msg.content)

# User input
question = st.chat_input("Ask a question...")

if question:

    # Show user message
    with st.chat_message("user"):
        st.write(question)

    st.session_state.chat_history.append(
        HumanMessage(content=question)
    )

    # Get response
    result = model.invoke(
        st.session_state.chat_history
    )

    # Show bot response
    with st.chat_message("assistant"):
        st.write(result.content)

    st.session_state.chat_history.append(
        AIMessage(content=result.content)
    )
