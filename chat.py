import streamlit as st
from shared import model_choice
from langchain.schema import HumanMessage, AIMessage

def render():
  st.header("Chat com o assistente 🤖")
  model = model_choice(st.session_state.model_class)

  if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

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
      response = model.invoke(user_query)  # Chama a função que retorna a resposta
      st.markdown(response.content)

    # Armazena a resposta corretamente no histórico
    st.session_state.chat_history.append(AIMessage(content=response.content))  # Salva apenas o conteúdo de texto gerado