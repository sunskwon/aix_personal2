import os
import torch
from datetime import datetime
from dotenv import load_dotenv
from embedchain import App
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings

os.environ["OLLAMA_HOST"] = "http://localhost:11434"
app = App.from_config(config_path="config.yaml")
app.reset()

if __name__ == '__main__':
    
    document1 = app.db.get()
    print(len(document1))

    query = "이석증이란?"
    url = 'https://www.nhis.or.kr/nhis/healthin/wbhace05000m01.do?mode=view&articleNo=10837408&article.offset=90&articleLimit=10'
    
    add_start_time = datetime.now()
    # print(f"add started at {add_start_time}")
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
    print(answer)
    
    document2 = app.db.get()
    print(len(document2))
    app.db.reset()

    
