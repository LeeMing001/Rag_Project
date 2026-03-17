#内部向量存储的使用
#再langchain内部有一个InMemoryVectorSore
#文本转向量模型
#添加向量add_documents添加
#删除向量
#相似性搜索

#外部向量存储的使用，外部库
from langchain_chroma import Chroma
#内存向量存储
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_community.embeddings import DashScopeEmbeddings #通义千问的嵌入模型
from langchain_community.document_loaders import CSVLoader
import os
import dotenv
dotenv.load_dotenv()
os.environ["DASHSCOPE_API_KEY"] = os.getenv("MY_QIANWEN_KEY")
# vector_store=InMemoryVectorStore(embedding=DashScopeEmbeddings())
vector_store = Chroma(
    collection_name="test" ,#给当前存储起个名字，类似数据库表的名字
    embedding_function=DashScopeEmbeddings(),
    persist_directory="./chroma_db"
)
loader=CSVLoader(
    file_path="../data/external/data_2.csv",
    encoding="utf-8",
    source_column="source",#指定本条数据的来源
)
documents=loader.load()
print(documents[0])
vector_store.add_documents(
    documents=documents,
    ids=["id"+str(i) for i in range(1,len(documents)+1)] #列表生成推导式
)

#删除
vector_store.delete(["id1","id2"])
#检索,返回类型list[Document]
result=vector_store.similarity_search(
    "美的空调评价好",
    3,
    filter={"source":"抖音"}
)
print(result)

