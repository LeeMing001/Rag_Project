#内存的rag+用户提问
from langchain_community.llms.tongyi import  Tongyi
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.embeddings import  DashScopeEmbeddings
from langchain_core.runnables import RunnablePassthrough
from langchain_core.vectorstores import InMemoryVectorStore
import os
import dotenv
from langchain_core.documents import Document
dotenv.load_dotenv()
os.environ["DASHSCOPE_API_KEY"]=os.getenv("MY_QIANWEN_KEY")

#大模型
llm=Tongyi(
    model="qwen-max"
)
#嵌入模型
emb=DashScopeEmbeddings(model="text-embedding-v4")
print(type(emb))
vector_stores=InMemoryVectorStore(embedding=emb)
#InMemoryVectorStore()对象不是Runnable对象，无法直接入链
#langchain中向量存储对象，有一个方法as_retriever，可以返回Runnable子类实例对象

#提示词
prompt=ChatPromptTemplate.from_messages(
    [
        ("system","你是一个AI助手，你的回答很简洁，请根据以下内容{rag}，回答用户问题"),
        ("human","{question}")
    ]
)
#提示词向量化
vector_stores.add_texts([
    "产后减肥要少吃多练",
    "在减肥期间怎么吃东西很重要，要少油少盐",
    "对于产后修复来说，游泳和瑜伽都是不错的运动方式"
])
user_input="产后怎么减肥"

# res=vector_stores.similarity_search(user_input,k=2)
retriever=vector_stores.as_retriever(search_kwargs={"k":2})
# reference_text="["
# for doc in res:
#     reference_text+=doc.page_content
# reference_text+="]"
def print_prompt(prompt):
    print("-" * 20)
    print(prompt.to_string())
    print("-"*20)
    return prompt
# chain=retriever|prompt|print_prompt|llm|StrOutputParser()
def format_func(docs:list[Document]):
    if not docs:
        return "无参考资料"
    formated_str="["
    for doc in docs:
        formated_str+=doc.page_content
    formated_str+=']'
    return formated_str

chain=(
    {"question":RunnablePassthrough(),"rag":retriever|format_func}|prompt|llm|StrOutputParser()
)
"""
retriever:
    -输入：用户的提问 str
    -输出：从向量库中检索的结果   List[Document]不含用户提问
prompt:
    -输入：用户的提问+向量库检索结果  dict
    -输出：完整的提示词             PromptValue

"""

# response=chain.invoke({"question":user_input,"rag":reference_text})
response=chain.invoke(user_input)
print(response)