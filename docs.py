import streamlit as st
from shared import model_choice, ModelClass
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import ChatPromptTemplate, PromptTemplate
from langchain_core.prompts import MessagesPlaceholder
from langchain.chains.retrieval import create_retrieval_chain
from langchain.chains.history_aware_retriever import create_history_aware_retriever
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.schema import HumanMessage, AIMessage


import os
import tempfile
from enum import Enum
import time

class PromptType(Enum):
  CONTEXT = "CONTEXT"
  QA = "QA"

def session_flow():
  if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
      AIMessage(content="Olá, sou um assistente virtual! Como posso ajudar?")
    ]
  
  if "docs_list" not in st.session_state:
    st.session_state.docs_list = None

  if "retriever" not in st.session_state:
    st.session_state.retriever = None

# Fluxo de upload
def upload_flow():
  uploads = st.sidebar.file_uploader(
    label="Enviar arquivos",
    type=["pdf"],
    accept_multiple_files=True
  )
  
  if not uploads:
    st.info("Envie um ou mais arquivos PDF para começar a conversa.")
    st.stop()
  
  return uploads

# Carrega PDFs enviados pelo usuário, salva temporariamente no disco
# e transforma cada um em documentos utilizáveis pelo LangChain
def config_retriever(uploads):
  docs = []
  temp_dir = tempfile.TemporaryDirectory()  # Cria um diretório temporário para armazenar os arquivos

  for file in uploads:
    temp_filepath = os.path.join(temp_dir.name, file.name)  # Cria o caminho temporário para cada arquivo
    with open(temp_filepath, "wb") as f:
      f.write(file.getbuffer())  # Salva o conteúdo do arquivo temporariamente

    loader = PyPDFLoader(temp_filepath)  # Carrega o PDF
    docs.extend(loader.load())  # Adiciona o conteúdo carregado à lista de documentos

  text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)  # Divide os documentos em pedaços menores
  splits = text_splitter.split_documents(docs)  # Realiza a divisão real dos documentos

  embeddings = HuggingFaceEmbeddings(model_name="BAAI/bge-m3")  # Embeddings para transformação de texto

  vectorstore = FAISS.from_documents(splits, embeddings)  # Armazena os documentos vetorizados no FAISS
  vectorstore.save_local("vectorstore/db_faiss")  # Salva o vetor no diretório local

  retriever = vectorstore.as_retriever(
    search_type="mmr",  # Tipo de busca (Maximum Marginal Relevance)
    search_kwargs={"k": 3, "fetch_k": 4}  # Configura parâmetros de busca
  )
  return retriever  # Retorna o retriever configurado
  
# Define o prompt de contextualização
def context_prompt(token_s, token_e):
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
  return context_q_prompt

# Define o prompt de perguntas e respostas (QA: Question & Answer)
def qa_prompt(token_s, token_e):
  qa_prompt_template = """Você é um assistente virtual prestativo e está respondendo perguntas gerais.
  Use os seguintes pedaços de contexto recuperado para responder à pergunta.
  Se você não sabe a resposta, apenas diga que não sabe. Mantenha a resposta concisa.
  Responda em português. \n\n
  Pergunta: {input} \n
  Contexto: {context}"""

  qa_prompt = PromptTemplate.from_template(token_s + qa_prompt_template + token_e)
  return qa_prompt

# Retorna o prompt com base no type
def prompt_define(model_class, type: PromptType):
  if model_class.model == ModelClass.HF_HUB:
    token_s, token_e = "<|begin_of_text|><|start_header_id|>system<|end_header_id|>", "<|eot_id|><|start_header_id|>assistant<|end_header_id|>"
  else:
    token_s, token_e = "", ""

  if type == PromptType.CONTEXT:
    context_q_prompt = context_prompt(token_s, token_e);
    return context_q_prompt
  
  elif type == PromptType.QA:
    prompt = qa_prompt(token_s, token_e)
    return prompt
  
def config_rag_chain(model, retriever):
  context_prompt = prompt_define(model, PromptType.CONTEXT)
  history_aware_retriever = create_history_aware_retriever(llm=model, retriever=retriever, prompt=context_prompt)

  # Configurar Chain para perguntas e respostas (Q&A)
  qa_prompt = prompt_define(model, PromptType.QA)
  qa_chain = create_stuff_documents_chain(model, qa_prompt)

  rag_chain = create_retrieval_chain(
    history_aware_retriever,
    qa_chain,
  )
  return rag_chain

#Mostrar a fonte da resposta
def show_source(result):
  sources = result["context"]
  for idx, doc in enumerate(sources):
    source = doc.metadata["source"]
    file = os.path.basename(source)
    page = doc.metadata.get("page", "Página não especificada")

    ref = f":link: Fonte {idx}: *{file} - p. {page}*"
    with st.popover(ref):
      st.caption(doc.page_content)

def render():
  st.header("Fale com seus documentos")
  uploads = upload_flow()
  session_flow()
  
  # Exibe o histórico de mensagens
  for message in st.session_state.chat_history:
    with st.chat_message("AI" if isinstance(message, AIMessage) else "Human"):
      st.write(message.content)

  start = time.time()
  user_query = st.chat_input("Digite sua mensagem...")
  model_class = model_choice(st.session_state.model_class)

  if user_query is not None and user_query != "" and uploads is not None:
    st.session_state.chat_history.append(HumanMessage(content=user_query))

    with st.chat_message("Human"):
      st.markdown(user_query)

    with st.chat_message("AI"):
      if st.session_state.docs_list != uploads:
        st.session_state.docs_list = uploads
        st.session_state.retriever = config_retriever(uploads)
      
      rag_chain = config_rag_chain(model_class, st.session_state.retriever)
      
      result =  rag_chain.invoke({"input": user_query, "chat_history": st.session_state.chat_history})
      resp =  result["answer"]

      st.write(resp)
      show_source(result)
    st.session_state.chat_history.append(AIMessage(content=resp))
  end = time.time()
  print(f"Tempo de execução: {end - start:.2f} segundos")
