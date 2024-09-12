import os
import torch
from datetime import datetime
from embedchain import App
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
if __name__ == '__main__':
    import crawling_research
else:
    from . import crawling_research

os.environ["OLLAMA_HOST"] = "http://localhost:11434"
app = App.from_config(config_path="config.yaml")
embeddings = HuggingFaceEmbeddings(
    model_name = "BAAI/bge-m3",
    model_kwargs = {'device': 'cuda' if torch.cuda.is_available() else 'cpu'},
    encode_kwargs = {'normalize_embeddings': True},
)
research_list = crawling_research.craw_research_list()
storage_start_time = datetime.now()
print(f"storage started at {storage_start_time}")
vector_store = FAISS.from_documents(documents = research_list, embedding = embeddings)
retriever = vector_store.as_retriever(search_type = 'similarity', search_kwargs = {'k': 1})
storage_end_time = datetime.now()
print(f"storage ended at {storage_end_time}")
print(f"storage time duration: {storage_end_time - storage_start_time}")

def answer_rag(query):
    
    app.reset()
    app.db.reset()
    
    retriever_start_time = datetime.now()
    # print(f"retrieve started at {retriever_start_time}")
    research = retriever.invoke(query)
    retriever_end_time = datetime.now()
    # print(f"retrieve ended at {retriever_end_time}")
    # print(f"retrieve time duration: {retriever_end_time - retriever_start_time}")
    research_url = research[0].metadata['source']
    
    add_start_time = datetime.now()
    # print(f"add started at {add_start_time}")
    app.add(research_url)
    add_end_time = datetime.now()
    # print(f"add ended at {add_end_time}")
    print(f"add time duration: {add_end_time - add_start_time}")
    
    generation_start_time = datetime.now()
    print(f"generation started at {generation_start_time}")
    answer = app.query(query)
    generation_end_time = datetime.now()
    print(f"generation ended at {generation_end_time}")
    print(f"generation time duration: {generation_end_time - generation_start_time}")
    
    return answer

if __name__ == '__main__':

    query = "쯔쯔가무시의 증상은?"
    
    result = answer_rag(query)
    print(result)