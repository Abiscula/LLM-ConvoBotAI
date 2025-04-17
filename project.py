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

def model_response(user_query, chat_history):
  llm = model_choice()

  # Definição dos prompts
  system_prompt = """
    Você é um assistente prestativo e está responedndo perguntas gerais responda em {language}
  """
  language = "portugues"

  if model_class.startswith("hf"):
    user_prompt = "<|begin_of_text|><|start_header_id|>user<|end_header_id|>\n{input}<|eot_id|><|start_header_id|>assistant<|end_header_id|>"
  else:
    user_prompt = "{input}"
  
  prompt_template = ChatPromptTemplate.from_messages([
    ("system", system_prompt),
    MessagesPlaceholder(variable_name="chat_history"),
    ("user", user_prompt)
  ])

  # Criação da Chain
  chain = prompt_template | llm | StrOutputParser()

  # Retorno da resposta / Stream
  # Diferente do .invoke o .stream retorna a mensagem em tempo real (durante a construção)
  return chain.stream({
    "chat_history": chat_history,
    "input": user_query,
    "language": language
  })
