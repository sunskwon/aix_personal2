import requests
from bs4 import BeautifulSoup
from langchain.schema import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

text_splitter = RecursiveCharacterTextSplitter(chunk_size=200, chunk_overlap=40)

def load_from_web(url):
    
    html = requests.get(url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"})
    soup = BeautifulSoup(html.text, "lxml")
    div_content = soup.find(class_='content_full clearfix')
    
    if div_content:
        paragraphs = div_content.find_all('p')
        
        text = ' '.join(p.text for p in paragraphs)
        
        document = Document(
            page_content=text,
            metadata={'source': url}
        )
        
        return [document]

def splt_text(data):
    
    return text_splitter.split_documents(data)

if __name__ == '__main__':
    url = 'https://www.nia.nih.gov/news/tdp-43-function-lost-decade-before-late-disease-onset'
    response = load_from_web(url)
    results = splt_text(response)
    for result in results:
        print(result)