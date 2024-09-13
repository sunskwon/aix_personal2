import bs4
from langchain_community.document_loaders import WebBaseLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

text_splitter = RecursiveCharacterTextSplitter(chunk_size=150, chunk_overlap=30)

def load_from_nia_web(url):
    
    loader = WebBaseLoader(
        web_path=url,
        bs_kwargs=dict(
            parse_only=bs4.SoupStrainer(
                
            )
        ),
    )
    
    print(loader.load())
    
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

def split_text(data):
    
    return text_splitter.split_documents(data)

if __name__ == '__main__':
    
    # url = "https://n.news.naver.com/mnews/article/031/0000869636"
    
    url = 'https://www.nia.nih.gov/news/scientists-identify-gene-variant-may-protect-against-apoe-e4-related-alzheimers-risk'
    data = load_from_nia_web(url)

    # url = 'https://www.nhis.or.kr/nhis/healthin/wbhace05000m01.do?mode=view&articleNo=10841895&article.offset=0&articleLimit=10'
    # data = load_from_nhis_web(url)

    result = split_text(data)
    print(data)