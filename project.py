import streamlit as st

import platform
from enum import Enum

from langchain_core.messages import AIMessage, HumanMessage
from langchain_ollama import ChatOllama
from langchain_core.prompts import MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_huggingface import HuggingFaceEndpoint

from config import load_config
from local_model import create_pipeline

# Carrega configurações e token da Hugging Face
config = load_config()
hf_token = config['HF_TOKEN']

# Configurações Streamlit
st.set_page_config(page_title="Assistente virtual 🤖", page_icon="🤖")
st.title("Assistente virtual 🤖")

# Enum para tipos de modelo
class ModelClass(Enum):
  HF_HUB = "hf_hub"
  LOCAL = "local"
  OLLAMA = "ollama"

# Wrapper simples para modelo local compatível com LangChain
class LocalPipelineWrapper:
  def __init__(self, pipeline):
    self.pipeline = pipeline

  def invoke(self, input, **kwargs):
    if isinstance(input, dict):
      input = input.get("input", "")
    result = self.pipeline(input)
    return result[0]["generated_text"]

# Função para seleção do modelo com uso de session_state
def select_model_class():
  if "model_class" not in st.session_state:
    st.session_state.model_class = ModelClass.HF_HUB

  # Condicional para exibir a opção de modelo local apenas no Windows
  if platform.system() == "Windows":
    selected_model = st.selectbox(
      "Escolha o modelo:",
      options=list(ModelClass),
      format_func=lambda m: (
        "Hugging Face" if m == ModelClass.HF_HUB else
        "Local (Phi-3)" if m == ModelClass.LOCAL else
        "Ollama"
      ),
      index=0 if st.session_state.model_class == ModelClass.HF_HUB
             else 1 if st.session_state.model_class == ModelClass.LOCAL
             else 2
    )
  else:  # Para Mac e outros sistemas, exibe apenas Hugging Face e Ollama
    selected_model = st.selectbox(
      "Escolha o modelo:",
      options=[ModelClass.HF_HUB, ModelClass.OLLAMA],  # Exclui o modelo LOCAL
      format_func=lambda m: (
        "Hugging Face" if m == ModelClass.HF_HUB else
        "Ollama"
      ),
      index=0 if st.session_state.model_class == ModelClass.HF_HUB
             else 1
    )

  st.session_state.model_class = selected_model
  return selected_model

# Seleção do modelo
model_class = select_model_class()

# Funções para carregar os modelos
def model_hf_hub(model="meta-llama/Meta-Llama-3-8B-Instruct", temperature=0.1):
  return HuggingFaceEndpoint(
    repo_id=model,
    max_new_tokens=512,
    return_full_text=False,
    huggingfacehub_api_token=hf_token
  )

def model_local():
  pipe = create_pipeline()
  return LocalPipelineWrapper(pipe)

def model_ollama(model="phi3", temperature=0.1):
  llm = ChatOllama(model=model, temperature=temperature)
  return llm

# Seleciona o modelo com base na escolha do usuário
def model_choice(model_class):
  if model_class == ModelClass.HF_HUB:
    return model_hf_hub()
  elif model_class == ModelClass.LOCAL:
    return model_local()
  elif model_class == ModelClass.OLLAMA:
    return model_ollama()

# Função que retorna a resposta da IA
def model_response(user_query, chat_history, model_class):
  llm = model_choice(model_class)

  system_prompt = "Você é um assistente prestativo e está respondendo perguntas gerais. Responda em {language}."
  language = "português"

  user_prompt = (
    "<|begin_of_text|><|start_header_id|>user<|end_header_id|>\n{input}"
    "<|eot_id|><|start_header_id|>assistant<|end_header_id|>"
    if model_class == ModelClass.HF_HUB else "{input}"
  )

  prompt_template = ChatPromptTemplate.from_messages([
    ("system", system_prompt),
    MessagesPlaceholder(variable_name="chat_history"),
    ("user", user_prompt)
  ])

  chain = prompt_template | llm | StrOutputParser()

  return chain.stream({
    "chat_history": chat_history,
    "input": user_query,
    "language": language
  })

# Inicializa o histórico de chat
if "chat_history" not in st.session_state:
  st.session_state.chat_history = [AIMessage(content="Olá! Sou seu assistente virtual. Como posso ajudar?")]

# Exibe o histórico de mensagens
for message in st.session_state.chat_history:
  with st.chat_message("AI" if isinstance(message, AIMessage) else "Human"):
    st.write(message.content)

# Input do usuário
user_query = st.chat_input("Digite sua mensagem aqui")
if user_query:
  st.session_state.chat_history.append(HumanMessage(content=user_query))

  with st.chat_message("Human"):
    st.markdown(user_query)

  with st.chat_message("AI"):
    response = st.write_stream(model_response(user_query, st.session_state.chat_history, model_class))

  st.session_state.chat_history.append(AIMessage(content=response))