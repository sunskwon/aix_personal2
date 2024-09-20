import os
import torch
from datetime import datetime
# from embedchain import App
from langchain_community.chat_models import ChatOllama
from langchain_community.vectorstores import FAISS
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_huggingface import HuggingFaceEmbeddings
if __name__ == '__main__':
    import crawling_research, split_text
else:
    from . import crawling_research, split_text

# os.environ["OLLAMA_HOST"] = "http://localhost:11434"
# script_dir = os.path.dirname(__file__)
# config_path = os.path.join(script_dir, '..', 'config.yaml')
# app = App.from_config(config_path=config_path)
embeddings = HuggingFaceEmbeddings(
    model_name = "BAAI/bge-m3",
    model_kwargs = {'device': 'cuda' if torch.cuda.is_available() else 'cpu'},
    encode_kwargs = {'normalize_embeddings': True},
)
llm = ChatOllama(model="gemma2:2b", temperature=0.2, top_k=30, top_p=0.8)

prompt = PromptTemplate.from_template(
"""
당신은 질문(question)에 대해 답변(Question-Answering)을 수행하는 친절한 AI 어시스턴트입니다.
당신의 임무는 주어진 문맥(context)을 바탕으로 질문(question)에 답하는 것입니다.
검색된 다음 문맥(context)을 사용하여 질문(question)에 답하세요.
만약, 주어진 문맥(context)에서 질문(question)에 대한 답을 찾을 수 없다면 `질문에 대한 정보를 찾을 수 없습니다` 라고 답하세요.
만약, 문맥(context)이 주어지지 않으면 '질문에 대한 정보를 찾을 수 없습니다' 라고 답하세요.
한글로만 답변하세요.
단, 기술적인 용어나 이름은 번역하지 않고 그대로 사용해 주세요.
Don't narrate the answer, just answer the question.
Let's think step-by-step.

#Question: 
{question} 

#Context: 
{context} 

#Answer:
"""
)

# research_list = crawling_research.craw_research_list()
research_list = crawling_research.craw_research_from_nhis(0)
research_list.extend(crawling_research.craw_research_from_nia(0))

storage_start_time = datetime.now()
print(f"storage started at {storage_start_time}")
vector_store = FAISS.from_documents(documents = research_list, embedding = embeddings)
retriever = vector_store.as_retriever(search_type = 'similarity', search_kwargs = {'k': 1})
storage_end_time = datetime.now()
print(f"storage ended at {storage_end_time}")
print(f"storage time duration: {storage_end_time - storage_start_time}")

def answer_rag(query):
    
    # app.reset()
    # app.db.reset()
    
    retriever_start_time = datetime.now()
    # print(f"retrieve started at {retriever_start_time}")
    research = retriever.invoke(query)
    # print(f"title: {research[0].page_content}")
    retriever_end_time = datetime.now()
    # print(f"retrieve ended at {retriever_end_time}")
    # print(f"retrieve time duration: {retriever_end_time - retriever_start_time}")
    research_url = research[0].metadata['source']
    
    if "https://www.nia.nih.gov/" in research_url:
        data = crawling_research.research_content_from_nia(research_url)

    elif "https://www.nhis.or.kr/" in research_url:
        data = split_text.load_from_nhis_web(research_url)
    
    split_lst = split_text.split_text(data)
    
    add_start_time = datetime.now()
    # print(f"add started at {add_start_time}")
    # app.add(research_url, data_type='web_page')
    temp_store = FAISS.from_documents(documents = split_lst, embedding = embeddings)
    # temp_retriever = temp_store.as_retriever(search_type = 'similarity', search_kwargs = {'k': 2})
    temp_retriever = temp_store.as_retriever(search_type = 'similarity_score_threshold', search_kwargs = {'score_threshold': 0.8})
    references= temp_retriever.invoke(query)
    for reference in references:
        print(f"reference: {reference}")
    # print(f"distances: {distances}")
    add_end_time = datetime.now()
    # for distance in distances:
    #     print(distance)
    # print(f"add ended at {add_end_time}")
    print(f"add time duration: {add_end_time - add_start_time}")
    
    chain = (
        {"context": temp_retriever, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )
    
    generation_start_time = datetime.now()
    print(f"generation started at {generation_start_time}")
    # answer = app.chat(query)
    answer = chain.invoke(query)
    generation_end_time = datetime.now()
    print(f"generation ended at {generation_end_time}")
    print(f"generation time duration: {generation_end_time - generation_start_time}")
    
    return answer

if __name__ == '__main__':

    query = "안면마비 증상의 원인?"
    
    result = answer_rag(query)
    print(result)