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
from dotenv import load_dotenv
from openai import OpenAI
from tenacity import (
    retry,
    stop_after_attempt,
    wait_random_exponential,
)  # for exponential backoff

#secrets!!
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
openai.api_key = api_key


#initialize connection with openAI
client = OpenAI()

@retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(6))
def completion_with_backoff(input_prompt):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a fancy, eccentric, and eloquently spoken tutor named S.T.I.M. (which stand for Shitty Tutor I made) with a skill for explainining complex and elementary concepts in simple terms. Where possible use popular teaching methods to improve user experience. You are designed to output JSON and keep response as the only variable in the content section."},
            {"role": "user", "content": input_prompt}
  ],
  stream=True,
)
    return response

def reset_conversation():
    del st.session_state.messages





"""

@retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(6))
def completion_with_backoff(input_prompt):
    return client.chat.completions.create(
      model="gpt-3.5-turbo",
      response_format={"type" : "json_object"},
      messages=[
        {"role": "system", "content": "You are a fancy, eccentric, and eloquently spoken tutor named S.T.I.M. (which stand for Shit Tutor I made) with a skill for explainining complex and elementary concepts in simple terms. Where possible use popular teaching methods like mnemonics, learning games, and suggestions of further topics to improve user experience. You output JSON."},
        {"role": "user", "content": prompt}
        ]
  )



  response = client.chat.completions.create(
  model="gpt-3.5-turbo",
  response_format={"type" : "json_object"},
  messages=[
    {"role": "system", "content": "You are a fancy, eccentric, and eloquently spoken tutor named S.T.I.M. (which stand for Shitty Tutor I made) with a skill for explainining complex and elementary concepts in simple terms. Where possible use popular teaching methods to improve user experience. You are designed to output JSON and keep response as the only variable in the content section."},
    {"role": "user", "content": prompt}
  ]
)

"""