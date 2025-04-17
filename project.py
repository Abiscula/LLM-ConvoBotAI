import streamlit as st
from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.prompts import MessagesPlaceholder

from langchain_ollama import ChatOllama

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

import torch
from langchain_huggingface import ChatHuggingFace
from langchain_huggingface import HuggingFaceEndpoint

from enum import Enum


from config import load_config

config = load_config()
hf_token = config['HF_TOKEN']

# Configurações streamlit
st.set_page_config(page_title="Assistente virtual 🤖", page_icon="🤖")
st.title("Assistente virtual 🤖")
# st.button("Botão")
# st.chat_input("Digite sua mensagem")

class ModelClass(Enum):
  HF_HUB = "hf_hub"
  OLLAMA = "ollama"

model_class = ModelClass.HF_HUB

def model_hf_hub(model="meta-llama/Meta-Llama-3-8B-Instruct", temperature=0.1):
  llm = HuggingFaceEndpoint(repo_id=model,
                            model_kwargs={
                              "temperatura": temperature,
                              "return_full_text": False,
                              "max_new_tokens": 512
                            })
  return llm

def model_ollama(model="phi3", temperature=0.1):
  llm = ChatOllama(model=model, temperature=temperature)
  return llm

def model_choice(model_class):
  #carrega a llm
  if model_class == ModelClass.HF_HUB:
    llm = model_hf_hub()
  elif model_class == ModelClass.OLLAMA:
    llm = model_ollama()

  return llm

def model_response(user_query, chat_history, ):
  llm = model_choice()