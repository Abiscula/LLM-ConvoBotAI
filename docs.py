import streamlit as st
from shared import model_choice

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

def render():
  st.header("Converse com documentos")
  upload_flow()
  model = model_choice(st.session_state.model_class)