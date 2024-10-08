import os
import torch
from datetime import datetime
from dotenv import load_dotenv
from embedchain import App
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings

os.environ["OLLAMA_HOST"] = "http://localhost:11434"
app = App.from_config(config_path="config.yaml")
embeddings = HuggingFaceEmbeddings(
    model_name = "BAAI/bge-m3",
    model_kwargs = {'device': 'cuda' if torch.cuda.is_available() else 'cpu'},
    encode_kwargs = {'normalize_embeddings': True},
)

if __name__ == '__main__':

    import crawling_research
    
    query = "칼로리 섭취를 줄이는게 건강에 영향을 주나요?"
    app.reset()
    app.db.reset()
    
    crawl_start_time = datetime.now()
    # print(f"crawling started at {crawl_start_time}")
    research_list = crawling_research.craw_research_list()
    crawl_end_time = datetime.now()
    # print(f"crawling ended at {crawl_end_time}")
    print(f"crawling time duration: {crawl_end_time - crawl_start_time}")
    
    retriever_start_time = datetime.now()
    # print(f"retrieve started at {retriever_start_time}")
    vector_store = FAISS.from_documents(documents = research_list, embedding = embeddings)
    retriever = vector_store.as_retriever(search_type = 'similarity', search_kwargs = {'k': 1})
    temps = retriever.invoke(query)
    retriever_end_time = datetime.now()
    # print(f"retrieve ended at {retriever_end_time}")
    print(f"retrieve time duration: {retriever_end_time - retriever_start_time}")
    
    add_start_time = datetime.now()
    # print(f"add started at {add_start_time}")
    for temp in temps:
        url = temp.metadata['source']
        app.add(url)
    add_end_time = datetime.now()
    # print(f"add ended at {add_end_time}")
    print(f"add time duration: {add_end_time - add_start_time}")
    
    generation_start_time = datetime.now()
    print(f"generation started at {generation_start_time}")
    answer = app.query(query)
    generation_end_time = datetime.now()
    print(f"generation ended at {generation_end_time}")
    print(f"generation time duration: {generation_end_time - generation_start_time}")
    # for temp in temps:
    #     print(temp)
    for temp in temps:
        print(temp)
    print(answer)
    # document = app.db.get()
    # print(document)
    
