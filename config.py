import os
from dotenv import load_dotenv

load_dotenv()

def load_config():
  hf_token = os.getenv('HF_TOKEN')
  if not hf_token:
    raise ValueError("HF_TOKEN não encontrado nas variáveis de ambiente.")
  return {
    'HF_TOKEN': hf_token
  }