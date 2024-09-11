import requests
from bs4 import BeautifulSoup
from datetime import datetime
from langchain.schema import Document
from langchain_community.document_loaders import WebBaseLoader

def craw_research_from_nhis(page):
    
    url = f"https://www.nhis.or.kr/nhis/healthin/wbhace05000m01.do?mode=list&&articleLimit=10&article.offset={page * 10}"
    
    html = requests.get(url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"})
    soup = BeautifulSoup(html.text, "lxml")
    title_list = soup.find_all('a', class_="a-link")
    
    research_list = []
    for title in title_list:
        if 'href' in title.attrs:
            data = {'title': ' '.join(title.text.split()), 'metadata': {'source': 'https://www.nhis.or.kr/nhis/healthin/wbhace05000m01.do' + title['href']}}
            document = Document(
                page_content = data['title'],
                metadata = data['metadata'],
            )
            research_list.append(document)
        
    return research_list
    
def craw_research_from_nia(page):
    
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
    
    craw_start_time = datetime.now()
    print(f"crawling started at {craw_start_time}")
    nia_page = 0
    nhis_page = 0
    is_nia_empty = False
    is_nhis_empty = False
    research_list = []
    
    while not is_nia_empty:
        # print(f"nia_page: {nia_page}")
        temp_list = craw_research_from_nia(nia_page)
        
        if len(temp_list) > 0:
            research_list.extend(temp_list)
            nia_page += 1
        else:
            is_nia_empty = True
    
    while not is_nhis_empty:
        # print(f"nhis_page: {nhis_page}")
        temp_list = craw_research_from_nhis(nhis_page)
        
        if len(temp_list) > 0:
            research_list.extend(temp_list)
            nhis_page += 1
        else:
            is_nhis_empty = True
    
    craw_end_time = datetime.now()
    print(f"crawling ended at {craw_end_time}")
    print(f"crawling duration time: {craw_end_time - craw_start_time}")
            
    return research_list

if __name__ == '__main__':
    print(len(craw_research_list()))