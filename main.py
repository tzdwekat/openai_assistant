#imports
import openai
import streamlit as st
import aiohttp  # for making API calls concurrently
import argparse  # for running script from command line
import asyncio  # for running API calls concurrently
import json  # for saving results to a jsonl file
import logging  # for logging rate limit warnings and other messages
import os  # for reading API key
import dotenv
import re  # for matching endpoint from request URL
import tiktoken  # for counting tokens
import time  # for sleeping after rate limit is hit
import json_stream
from io import StringIO 
import io
import ast
from dotenv import load_dotenv
from openai import OpenAI
from tenacity import (
    retry,
    stop_after_attempt,
    wait_random_exponential,
)  # for exponential backoff
from functions import completion_with_backoff, reset_conversation

#secrets!!
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
openai.api_key = api_key

#initialize connection with openAI
client = OpenAI()

#Styling
st.markdown("<h1 style='text-align: center; color: white;'>S.T.I.M. The Tutor</h1>", unsafe_allow_html=True)
left_co, cent_co,last_co = st.columns(3)
with cent_co:
    st.image("./stim_head.png")
    st.button('Reset Chat', on_click=reset_conversation, use_container_width=True)
st.divider()
st.write("Hello, my name is S.T.I.M. (Shitty Tutor I Made), how can I help you today?")
    

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []
# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# React to user input
if prompt := st.chat_input("How may I assist you?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    with st.chat_message("assistant"):
        stream = completion_with_backoff(prompt)
        stream_dict = json.loads(stream.choices[0].message.content)
        stream_content = stream_dict["content"]
        response = st.write(stream_content)
    st.session_state.messages.append({"role": "assistant", "content": response})

