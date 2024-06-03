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

#get input
print("\nHello, my name is S.T.I.M. (Shitty Tutor I Made), how can I help you today?\n")
prompt = input("What would you like to learn?\n\n")


#the brains behind everything (the openAI api calls) eventually parallel prompt entering and rate limiting will be added)
response = client.chat.completions.create(
  model="gpt-3.5-turbo",
  response_format={"type" : "json_object"},
  messages=[
    {"role": "system", "content": "You are a fancy, eccentric, and eloquently spoken tutor named S.T.I.M. (which stand for Shitty Tutor I made) with a skill for explainining complex and elementary concepts in simple terms. Where possible use popular teaching methods to improve user experience. You are designed to output JSON and keep response as the only variable in the content section."},
    {"role": "user", "content": prompt}
  ]
)


print("\n")
response_output = json.loads(response.choices[0].message.content)
print(response_output["content"])
print("\n")

