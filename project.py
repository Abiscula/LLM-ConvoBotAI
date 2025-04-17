import streamlit as st
from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.prompts import MessagesPlaceholder

from langchain_ollama import ChatOllama

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

import torch
from langchain_huggingface import ChatHuggingFace
from langchain_huggingface import HuggingFaceEndpoint