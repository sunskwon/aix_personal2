from langchain_community.chat_models import ChatOllama
# from langchain_core.output_parsers import StrOutputParser
# from langchain_core.runnables import RunnablePassthrough

# # 모델 인스턴스화
# llm = ChatOllama(model="llama3.1:latest")

# # 체인 정의
# chain = (
#     llm
#     | StrOutputParser()
# )

# # 체인 호출 및 결과 출력
# try:
#     result = chain.invoke("explain about 'paris'")
#     print(result)
# except Exception as e:
#     print(f"An error occurred: {e}")

from langchain_core.prompts import ChatPromptTemplate

llm = ChatOllama(model="llama3.1:latest")
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful, professional assistant named 권봇. Introduce yourself first, and answer the questions. answer me in Korean no matter what. "),
    ("user", "{input}")
])

chain = prompt | llm
answer = chain.invoke({"input": "What is stock?"})

print(answer)