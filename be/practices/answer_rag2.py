import os
from dotenv import load_dotenv
# Replace this with your HF token

load_dotenv()

SECRET_ENV = os.getenv("HUGGING_FACE_TOKEN")
os.environ["HUGGINGFACE_ACCESS_TOKEN"] = SECRET_ENV

from embedchain import App

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
app.add("https://www.forbes.com/profile/elon-musk")
app.add("https://en.wikipedia.org/wiki/Elon_Musk")
# app.add("https://www.nia.nih.gov/news/research-highlights?page=0")
# app.add("https://www.nia.nih.gov/news/smartphone-based-cognitive-testing-app-reliably-predicted-diagnosed-ftld")
answer = app.query("what is accurate blood test?" + " answer in korean")
print(answer)


# Answer: The net worth of Elon Musk today is $258.7 billion.
