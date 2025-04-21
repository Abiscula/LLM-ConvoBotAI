import streamlit as st

st.set_page_config(page_title="Assistente virtual 🤖", page_icon="🤖")

import platform
from shared import ModelClass

def select_model_class():
  if "model_class" not in st.session_state:
    st.session_state.model_class = None

  if platform.system() == "Windows":
    model_options = list(ModelClass)
  else:
    model_options = [ModelClass.HF_HUB, ModelClass.OLLAMA]

  label_map = {
    ModelClass.HF_HUB: "Hugging Face",
    ModelClass.LOCAL: "Local (Phi-3)",
    ModelClass.OLLAMA: "Ollama"
  }

  display_options = ["Selecione um modelo..."] + [label_map[m] for m in model_options]
  selected_label = st.selectbox("Escolha o modelo:", display_options)

  if selected_label != "Selecione um modelo...":
    selected_model = model_options[display_options.index(selected_label) - 1]
    st.session_state.model_class = selected_model
  else:
    st.session_state.model_class = None
    st.session_state.flow_selected = None 

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

# Só mostra a opção de fluxo após o modelo ser selecionado
if st.session_state.model_class is not None:
  start_assistant()