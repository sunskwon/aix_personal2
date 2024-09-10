import os
import torch
from datetime import datetime
from dotenv import load_dotenv
from embedchain import App
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings

load_dotenv()
SECRET_ENV = os.getenv('HUGGINGFACE_ACCESS_TOKEN')

os.environ['HUGGINGFACE_ACCESS_TOKEN'] = SECRET_ENV
config = {
  'llm': {
    'provider': 'huggingface',
    'config': {
      'model': 'mistralai/Mistral-7B-Instruct-v0.2',
      'top_p': 0.5,
      'prompt': (
        #   "주어진 문맥(context)을 바탕으로 질문(question)에 답변하세요.\n"
        #   "주어진 문맥(context)에서 답을 찾을 수 없거나 답을 모른다면 `질문에 대한 정보를 찾을 수 없습니다` 라고 답하세요.\n"
        #   "Briefly answer in Korean.\n"
        #   "Answer in Korean\n"
        #   "Don't narrate the answer, just answer the question.\n"
          "context: $context\n\nquestion: $query\n\nHelpful Answer:"
      ),
    }
  },
  'embedder': {
    'provider': 'huggingface',
    'config': {
      'model': 'sentence-transformers/all-mpnet-base-v2',
    }
  }
}
app = App.from_config(config=config)
# app = App.from_config(config_path="config.yaml")
embeddings = HuggingFaceEmbeddings(
    model_name = "BAAI/bge-m3",
    model_kwargs = {'device': 'cuda' if torch.cuda.is_available() else 'cpu'},
    encode_kwargs = {'normalize_embeddings': True},
)

if __name__ == '__main__':

    import crawling_research
    
    query = "아스피린의 영향?"
    
    crawl_start_time = datetime.now()
    # print(f"crawling started at {crawl_start_time}")
    research_list = crawling_research.craw_research_list()
    crawl_end_time = datetime.now()
    # print(f"crawling ended at {crawl_end_time}")
    print(f"crawling time duration: {crawl_end_time - crawl_start_time}")
    
    retriever_start_time = datetime.now()
    # print(f"retrieve started at {retriever_start_time}")
    vector_store = FAISS.from_documents(documents = research_list, embedding = embeddings)
    retriever = vector_store.as_retriever(search_type = 'similarity', search_kwargs = {'k': 5})
    temps = retriever.invoke(query)
    retriever_end_time = datetime.now()
    # print(f"retrieve ended at {retriever_end_time}")
    print(f"retrieve time duration: {retriever_end_time - retriever_start_time}")
    
    add_start_time = datetime.now()
    # print(f"add started at {add_start_time}")
    for temp in temps:
        print(temp)
        app.add(temp.metadata['source'])
    add_end_time = datetime.now()
    # print(f"add ended at {add_end_time}")
    print(f"add time duration: {add_end_time - add_start_time}")
    
    inference_start_time = datetime.now()
    print(f"inference started at {inference_start_time}")
    answer = app.query(query)
    print(answer)
    inference_end_time = datetime.now()
    print(f"inference ended at {inference_end_time}")
    print(f"inference time duration: {inference_end_time - inference_start_time}")
    
