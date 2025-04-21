import streamlit as st
from shared import model_choice
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS

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
  



def render():
  st.header("Converse com documentos")
  uploads = upload_flow()
  retriever = config_retriever(uploads)
  model = model_choice(st.session_state.model_class)