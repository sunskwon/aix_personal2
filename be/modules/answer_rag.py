import torch
from langchain_community.chat_models import ChatOllama
from langchain_community.vectorstores import FAISS
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_huggingface import HuggingFaceEmbeddings

embeddings = HuggingFaceEmbeddings(
    model_name = "BAAI/bge-m3",
    model_kwargs = {'device': 'cuda' if torch.cuda.is_available() else 'cpu'},
    encode_kwargs = {'normalize_embeddings': True},
)
llm = ChatOllama(model='llama3.1:latest')

import crawling_research

research_list = crawling_research.craw_research_list()

vector_store = FAISS.from_documents(documents = research_list, embedding = embeddings)

retriever = vector_store.as_retriever(search_type = 'similarity', search_kwargs = {'k': 5})

temps = retriever.invoke('공간감을 향상하는 방법?')

for temp in temps:
    print(temp)