import streamlit as st
from google import genai
import requests
import os
from dotenv import load_dotenv

load_dotenv()
api_url = os.getenv("API_URL")

def ask_api(question):

    response = requests.post(f"{api_url}/ask", json={"text": question})
    response.raise_for_status()
    data = response.json()
    return data["answer"], data["sources"], data["usage"]


st.set_page_config(page_title="Electronics QA", page_icon=":robot_face:", layout="centered")
st.title("Electronics QA")

if "messages" not in st.session_state:
    st.session_state.messages = []

def show_sources(chunks):
    for c in chunks:
        st.markdown(f"**{c['source']}**")
        st.write(c['text'])

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if message["role"] == "assistant":
            show_sources(message["chunks"])

if prompt := st.chat_input("What do you wanna know about electronics?"):
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})


    with st.chat_message("assistant"):
        try:
            with st.spinner("Thinking..."):
                text, chunks, usage = ask_api(prompt)
        except Exception as e:
            st.error(f"Error: {e}")
            st.stop()

        st.markdown(text)
        show_sources(chunks)
        st.caption(f"Input tokens: {usage['input_tokens']}, Output tokens: {usage['output_tokens']}")

    st.session_state.messages.append({"role": "assistant", "content": text, "chunks": chunks})