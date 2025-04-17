import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline, BitsAndBytesConfig

from config import load_config


# Carrega configurações e token da Hugging Face
config = load_config()
hf_token = config['HF_TOKEN']


# Realiza a quantização do modelo para rodar em dispositivos mais leves
def quantization():
  quantization_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_use_double_quant=True,
    bnb_4bit_compute_dtype=torch.bfloat16
  )
  return quantization_config


def create_ai_model():
  model_id = 'microsoft/Phi-3-mini-4k-instruct'

  config = load_config()
  hf_token = config['HF_TOKEN']

  if not hf_token:
    pass

  quantization_config = quantization()

  model = AutoModelForCausalLM.from_pretrained(
    pretrained_model_name_or_path = model_id, 
    quantization_config = quantization_config,
    token = hf_token,
  )

  tokenizer = AutoTokenizer.from_pretrained(model_id)

  return [model, tokenizer]

def create_pipeline():
  [model, tokenizer] = create_ai_model()

  pipe = pipeline(
    model = model,
    tokenizer = tokenizer,
    task = "text-generation",
    temperature = 0.1,
    max_new_tokens = 500,
    do_sample = True,
    repetition_penalty = 1.1,
    return_full_text = False
  )

  return pipe