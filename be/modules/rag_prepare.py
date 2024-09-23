import bs4
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from langchain.schema import Document
from langchain_community.document_loaders import WebBaseLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

text_splitter = RecursiveCharacterTextSplitter(chunk_size=400, chunk_overlap=40)
    
def title_lst_from_nia(page_num):
    
    url = f"https://www.nia.nih.gov/news/research-highlights?page={page_num}"
    
    html = requests.get(url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"})
    soup = BeautifulSoup(html.text, "lxml")
    titles = soup.find_all("h3")
    
    title_list = []
    for title in titles:
        a = title.find("a")
        if 'href' in a.attrs:
            data = {'title': title.text, 'metadata': {'source': 'https://www.nia.nih.gov' + a['href']}}
            document = Document(
                page_content = data['title'],
                metadata = data['metadata'],
            )
            title_list.append(document)
            
    return title_list

def title_lst_from_nhis(page_num):
    
    url = f"https://www.nhis.or.kr/nhis/healthin/wbhace05000m01.do?mode=list&&articleLimit=10&article.offset={page_num * 10}"
    
    html = requests.get(url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"})
    soup = BeautifulSoup(html.text, "lxml")
    titles = soup.find_all('a', class_="a-link")
    
    title_list = []
    
    for title in titles:
        if 'href' in title.attrs:
            data = {'title': ' '.join(title.text.split()), 'metadata': {'source': 'https://www.nhis.or.kr/nhis/healthin/wbhace05000m01.do' + title['href']}}
            document = Document(
                page_content = data['title'],
                metadata = data['metadata'],
            )
            title_list.append(document)
        
    return title_list

def craw_title_list():
    
    craw_start_time = datetime.now()
    print(f"crawling started at {craw_start_time}")
    
    nia_page = 0
    nhis_page = 0
    is_nia_empty = False
    is_nhis_empty = False
    
    title_list = []
    
    while not is_nia_empty:
        print(f"nia_page: {nia_page}")
        temp_list = title_lst_from_nia(nia_page)
        
        if len(temp_list) > 0:
            title_list.extend(temp_list)
            nia_page += 1
        else:
            is_nia_empty = True
    
    while not is_nhis_empty:
        print(f"nhis_page: {nhis_page}")
        temp_list = title_lst_from_nhis(nhis_page)
        
        if len(temp_list) > 0:
            title_list.extend(temp_list)
            nhis_page += 1
        else:
            is_nhis_empty = True
    
    craw_end_time = datetime.now()
    print(f"crawling ended at {craw_end_time}")
    print(f"crawling duration time: {craw_end_time - craw_start_time}")
            
    return title_list

def content_from_nia(url):
    
    content_selector = ".content_full"
    
    html = requests.get(url, headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"})
    soup = BeautifulSoup(html.text, "lxml")
    
    content = soup.select(content_selector)
    content_lst = []
    for c in content:
        c_text = c.text
        c_text = c_text.strip()
        content_lst.append(c_text)
    content_str = "".join(content_lst)
    
    document = Document(
        page_content = content_str,
        metadata = {'source': url}
    )
    
    return [document]

def content_from_nhis(url):
    
    content_selector = ".fr-view"
    
    html = requests.get(url, headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"})
    soup = BeautifulSoup(html.text, "lxml")
    
    content = soup.select(content_selector)
    content_lst = []
    for c in content:
        c_text = c.text
        c_text = c_text.strip()
        content_lst.append(c_text)
    content_str = "".join(content_lst)
    
    document = Document(
        page_content = content_str,
        metadata = {'source': url}
    )
    
    return [document]

def load_from_nia_web(url):
    
    loader = WebBaseLoader(
        web_path=url,
        bs_kwargs=dict(
            parse_only=bs4.SoupStrainer(
                
            )
        ),
    )
    
    return loader.load()

def load_from_nhis_web(url):
    
    loader = WebBaseLoader(
        web_path=url,
        bs_kwargs=dict(
            parse_only=bs4.SoupStrainer(
                attrs={"class": ["fr-view"]},
            )
        ),
    )
    
    return loader.load()

def split_text(document):
    
    return text_splitter.split_documents(document)

if __name__ == '__main__':

    title_list = title_lst_from_nia(0)
    title_list.extend(title_lst_from_nhis(0))

    content_list = []
    for title in title_list:
        url = title.metadata['source']
        if 'https://www.nia.nih.gov/' in url:
            content_list.append(content_from_nia(url))
        else:
            content_list.append(content_from_nhis(url))
    
    chunk_list = []
    for content in content_list:
        chunk_list.extend(split_text(content))

    print(chunk_list)