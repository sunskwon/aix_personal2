import os
from dotenv import load_dotenv
from embedchain import App
import crawling_research
from datetime import datetime

load_dotenv()
SECRET_ENV = os.getenv('HUGGINGFACE_ACCESS_TOKEN')

os.environ['HUGGINGFACE_ACCESS_TOKEN'] = SECRET_ENV
config = {
  'llm': {
    'provider': 'huggingface',
    'config': {
      'model': 'mistralai/Mistral-7B-Instruct-v0.2',
      'top_p': 0.5
    }
  },
  'embedder': {
    'provider': 'huggingface',
    'config': {
      'model': 'sentence-transformers/all-mpnet-base-v2'
    }
  }
}
app = App.from_config(config=config)

if __name__ == '__main__':
    
    crawl_start_time = datetime.now()
    print(f"crawling started at {crawl_start_time}")
    researches = crawling_research.craw_research_list()
    print(len(researches))
    crawl_end_time = datetime.now()
    print(f"crawling ended at {crawl_end_time}")
    print(f"crawling time duration: {crawl_end_time - crawl_start_time}")
    
    add_start_time = datetime.now()
    print(f"add started at {add_start_time}")
    for research in researches:
        app.add(research.metadata['source'])
    add_end_time = datetime.now()
    print(f"add ended at {add_end_time}")
    print(f"add time duration: {add_end_time - add_start_time}")
    