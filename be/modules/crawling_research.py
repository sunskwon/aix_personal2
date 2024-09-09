import requests
from bs4 import BeautifulSoup
from langchain.schema import Document
from langchain_community.document_loaders import WebBaseLoader

def craw_research(page):
    
    url = f"https://www.nia.nih.gov/news/research-highlights?page={page}"
    
    html = requests.get(url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"})
    soup = BeautifulSoup(html.text, "lxml")
    title_list = soup.find_all("h3")
    
    research_list = []
    for title in title_list:
        a = title.find("a")
        if 'href' in a.attrs:
            data = {'title': title.text, 'metadata': {'source': 'https://www.nia.nih.gov' + a['href']}}
            document = Document(
                page_content = data['title'],
                metadata = data['metadata'],
            )
            research_list.append(document)
            
    return research_list

def craw_research_list():
    
    page = 0
    is_empty = False
    research_list = []
    
    while not is_empty:
        temp_list = craw_research(page)
        
        if len(temp_list) > 0:
            research_list.extend(temp_list)
            page += 1
        else:
            is_empty = True
            
    return research_list

if __name__ == '__main__':
    craw_research_list()