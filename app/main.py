from fastapi import FastAPI
from rag import answer
import streamlit as st
from google import genai

app = FastAPI()

@app.post("/ask")
async def ask_question(question: str):
    return answer(question)

st.set_page_config(page_title="Electronics QA", page_icon=":robot_face:", layout="centered")
st.title("Electronics QA")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("What do you wanna know about electronics?"):
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})
