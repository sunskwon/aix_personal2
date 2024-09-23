import os
import torch
from datetime import datetime
# from embedchain import App
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
if __name__ == '__main__':
    import crawling_research
else:
    from ..modules import rag_prepare

os.environ["OLLAMA_HOST"] = "http://localhost:11434"
config = {
    'llm': {
        'provider': 'ollama',
        'config': {
            'model': 'gemma2:2b',
            'temperature': 0.5,
            'top_p': 1,
            'stream': True,
            'prompt': (
                "Use the following pieces of context to answer the query at the end.\n"
                "If you don't know the answer, just say that you don't know, don't try to make up an answer.\n"
                "$context\n\nQuery: $query\n\nHelpful Answer:"
            ),
            'base_url': 'http://localhost:11434'
        }
    },
    'vectordb': {
        'provider': 'chroma',
        'config': {
            'dir': 'db',
            'allow_reset': True
        }
    },
    'embedder': {
        'provider': 'ollama',
        'config': {
            'model': 'nomic-embed-text:latest',
        }
    }
}
# script_dir = os.path.dirname(__file__)
# config_path = os.path.join(script_dir, '..', 'config.yaml')
app = App.from_config(config=config)
embeddings = HuggingFaceEmbeddings(
    model_name = "BAAI/bge-m3",
    model_kwargs = {'device': 'cuda' if torch.cuda.is_available() else 'cpu'},
    encode_kwargs = {'normalize_embeddings': True},
)
# research_list = crawling_research.craw_research_list()
research_list = rag_prepare.craw_research_from_nhis(0)
storage_start_time = datetime.now()
print(f"storage started at {storage_start_time}")
vector_store = FAISS.from_documents(documents = research_list, embedding = embeddings)
retriever = vector_store.as_retriever(search_type = 'similarity', search_kwargs = {'k': 1})
storage_end_time = datetime.now()
print(f"storage ended at {storage_end_time}")
print(f"storage time duration: {storage_end_time - storage_start_time}")

def answer_rag(query):
    
    # app.reset()
    app.db.reset()
    
    retriever_start_time = datetime.now()
    # print(f"retrieve started at {retriever_start_time}")
    research = retriever.invoke(query)
    print(f"title: {research[0].page_content}")
    retriever_end_time = datetime.now()
    # print(f"retrieve ended at {retriever_end_time}")
    # print(f"retrieve time duration: {retriever_end_time - retriever_start_time}")
    research_url = research[0].metadata['source']
    
    add_start_time = datetime.now()
    # print(f"add started at {add_start_time}")
    app.add(research_url, data_type='web_page')
    add_end_time = datetime.now()
    # print(f"add ended at {add_end_time}")
    print(f"add time duration: {add_end_time - add_start_time}")
    
    generation_start_time = datetime.now()
    print(f"generation started at {generation_start_time}")
    answer = app.chat(query)
    generation_end_time = datetime.now()
    print(f"generation ended at {generation_end_time}")
    print(f"generation time duration: {generation_end_time - generation_start_time}")
    
    return answer

if __name__ == '__main__':

    query = "what is apple?"
    
    result = answer_rag(query)
    print(result)