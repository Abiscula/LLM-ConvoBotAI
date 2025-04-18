import streamlit as st

st.set_page_config(page_title="Assistente virtual 🤖", page_icon="🤖")

import platform
from shared import ModelClass

def select_model_class():
  if "model_class" not in st.session_state:
    st.session_state.model_class = ModelClass.HF_HUB

  if platform.system() == "Windows":
    selected_model = st.selectbox(
      "Escolha o modelo:",
      options=list(ModelClass),
      format_func=lambda m: (
        "Hugging Face" if m == ModelClass.HF_HUB else
        "Local (Phi-3)" if m == ModelClass.LOCAL else
        "Ollama"
      ),
      index=list(ModelClass).index(st.session_state.model_class)
    )
  else:
    available_models = [ModelClass.HF_HUB, ModelClass.OLLAMA]
    try:
      selected_index = available_models.index(st.session_state.model_class)
    except ValueError:
      selected_index = 0
      st.session_state.model_class = ModelClass.HF_HUB

    selected_model = st.selectbox(
      "Escolha o modelo:",
      options=available_models,
      format_func=lambda m: "Hugging Face" if m == ModelClass.HF_HUB else "Ollama",
      index=selected_index
    )

  st.session_state.model_class = selected_model
  return selected_model

def start_assistant():
  if "flow_selected" not in st.session_state:
    st.session_state.flow_selected = None

  if st.session_state.flow_selected is None:
    st.title("Assistente virtual 🤖")
    st.info("Olá! O que você deseja fazer?")
    option = st.radio("Escolha uma opção:", ["Conversar", "Acessar um arquivo"])

    if st.button("Confirmar"):
      if option == "Conversar":
        st.session_state.flow_selected = "chat"
      elif option == "Acessar um arquivo":
        st.session_state.flow_selected = "docs"
      st.rerun()

  elif st.session_state.flow_selected == "chat":
    import chat
    chat.render()

  elif st.session_state.flow_selected == "docs":
    import docs
    docs.render()

select_model_class()
start_assistant()