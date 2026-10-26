"""A tiny Streamlit chatbot used to demonstrate Docker.

The app reads OPENAI_API_KEY and OPENAI_MODEL from the environment.
Locally, python-dotenv loads them from a .env file.
In Docker, pass that file at startup with --env-file. It is not copied
into the image.
"""
import os

import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

st.set_page_config(page_title="GenAI ChatBot")

st.title("AI ChatBot")

st.write(
  ":rainbow[A simple chatbot for docker.]"
  ":raibow[Your message and chat history is sent to an OpenAI model and reply is shown below.]"
  ""
)

api_key = os.getenv("OPENAI_API_KEY").strip()
model = os.getenv("MODEL","gpt-4o-mini").strip()

st.caption(f":green[Model:{model}]")

if not api_key:
  st.error(
    "No OpenAI API key found. Copy .env, paste your key "
    "into OPENAI_API_KEY, and start the app again. When you use Docker, "
    "pass that file at runtime with --env-file .env."
  )
  st.stop()


# session_state keeps the conversation for this browser tab.
if "messages" not in st.session_state:
  st.session_state.messages = []

for msg in st.session_state.messages:
  st.chat_message(msg["role"]).markdown(msg["content"])

user_message = st.chat_input("Type message")
if not user_message:
  st.stop()

st.session_state.messages.append({"role":"user","content":user_message})

with st.chat_message("user"):
  st.markdown(user_message)


client = OpenAI(api_key=api_key)

try:

  with st.spinner("Waiting for the model..."):
    response = client.chat.completions.create(
      model=model,
      messages=[
        {
          "role":"system",
          "content": ("You are a helpful assistant in a beginner Docker and "
                     "GenAI class. Keep answers clear and short.")
        },
        *st.session_state.messages,
      ]
    )

    answer = response.choices[0].message.content or "(Model returned empty reply.)"

except Exception as error:
  st.error(
    "The OpenAI request failed. Check the API key, the model name, "
    f"and your network connection.\n\nDetails: {error}"
  )
  st.stop()

with st.chat_message("assistant"):
  st.markdown(answer)

st.session_state.messages.append({"role":"assistant", "content":answer})