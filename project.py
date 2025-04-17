import streamlit as st
from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.prompts import MessagesPlaceholder

from langchain_ollama import ChatOllama

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

import torch
from langchain_huggingface import ChatHuggingFace
from langchain_huggingface import HuggingFaceEndpoint

from config import load_config

config = load_config()
hf_token = config['HF_TOKEN']

# Configurações streamlit
st.set_page_config(page_title="Assistente virtual 🤖", page_icon="🤖")
st.title("Assistente virtual 🤖")
# st.button("Botão")
# st.chat_input("Digite sua mensagem")