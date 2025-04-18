from enum import Enum
from config import load_config
from local_model import create_pipeline

config = load_config()
hf_token = config['HF_TOKEN']

class ModelClass(Enum):
  HF_HUB = "hf_hub"
  LOCAL = "local"
  OLLAMA = "ollama"

class LocalPipelineWrapper:
  def __init__(self, pipeline):
    self.pipeline = pipeline

  def invoke(self, input, **kwargs):
    if isinstance(input, dict):
      input = input.get("input", "")
    result = self.pipeline(input)
    return result[0]["generated_text"]

# Modelo do huggingface
def model_hf_hub(model="meta-llama/Meta-Llama-3-8B-Instruct", temperature=0.1):
  from langchain_huggingface import HuggingFaceEndpoint
  return HuggingFaceEndpoint(
    repo_id=model,
    max_new_tokens=512,
    return_full_text=False,
    huggingfacehub_api_token=hf_token
  )

# Modelo será carregado localmente (windows)
def model_local():
  pipe = create_pipeline()
  return LocalPipelineWrapper(pipe)

# Modelo com ollama (precisa do servidor rodando)
def model_ollama(model="phi3", temperature=0.1):
  from langchain_ollama import ChatOllama
  return ChatOllama(model=model, temperature=temperature)

def model_choice(model_class):
  if model_class == ModelClass.HF_HUB:
    return model_hf_hub()
  elif model_class == ModelClass.LOCAL:
    return model_local()
  elif model_class == ModelClass.OLLAMA:
    return model_ollama()