import streamlit as st
from shared import model_choice, ModelClass
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import ChatPromptTemplate, PromptTemplate
from langchain_core.prompts import MessagesPlaceholder


import os
import tempfile

# Fluxo de upload
def upload_flow():
  uploads = st.sidebar.file_uploader(
    label="Enviar arquivos",
    type=["pdf"],
    accept_multiple_files=True
  )
  
  if not uploads:
    st.info("Por favor, envie algum arquivo para continuar")
    st.stop()
  
  return uploads


# Carrega PDFs enviados pelo usuário, salva temporariamente no disco
# e transforma cada um em documentos utilizáveis pelo LangChain
def config_retriever(uploads):
  docs = []
  temp_dir = tempfile.TemporaryDirectory() # Cria um diretorio temporario
  for file in uploads:
    temp_filepath = os.path.join(temp_dir.name, file.name) # Cria um caminho temporario
    with open(temp_filepath, "wb") as f:
      f.write(file.getValue())
    loader = PyPDFLoader(temp_filepath)
    docs.extend(loader.load()) # Carrega o arquivo e salva em docs (extend = foo.push(...arr) no js)

    # Split (Divisao dos docs em pedaços de texto)
    text_spitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    splits = text_spitter.split_documents(docs)

    # Embedding
    embeddings = HuggingFaceEmbeddings(model_name="BAAI/bge-m3")

    # Armazenamento
    vectorstore = FAISS.from_documents(splits, embeddings)
    vectorstore.save_local("vectorstore/db_faiss")

    # Configuração do retriever
    retriever = vectorstore.as_retriever(search_type = "mmr",
                                         search_kwargs = {"k": 3, "fetch_k": 4})
    
    return retriever
  

def prompt_define(model_class):
  if model_class.model == ModelClass.HF_HUB:
    token_s, token_e = "<|begin_of_text|><|start_header_id|>system<|end_header_id|>", "<|eot_id|><|start_header_id|>assistant<|end_header_id|>"
  else:
    token_s, token_e = "", ""

  # Prompt de contextualização
  context_q_system_prompt = "Given the following chat history and the follow-up question which might reference " \
  "context in the chat history, formulate a standalone question which can be understood without the chat history. " \
  "Do NOT answer the question, just reformulate it if needed and otherwise return it as is."

  context_q_system_prompt = token_s + context_q_system_prompt
  context_q_user_prompt = "Question: {input}" + token_e
  context_q_prompt = ChatPromptTemplate.from_messages(
    [
      ("system", context_q_system_prompt),
      MessagesPlaceholder("chat_history"),
      ("human", context_q_user_prompt),
    ]
  )
  return context_q_system_prompt, context_q_user_prompt, context_q_prompt
  
def config_rag_chain(model, retriever):
  system_prompt, user_prompt, context_prompt = prompt_define(model)

def render():
  st.header("Converse com documentos")
  uploads = upload_flow()
  retriever = config_retriever(uploads)
  model_class = model_choice(st.session_state.model_class)

  config_rag_chain(model_class, retriever)