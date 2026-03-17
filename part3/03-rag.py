#内存的rag+用户提问
from langchain_community.llms.tongyi import  Tongyi
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.embeddings import  DashScopeEmbeddings
from langchain_core.vectorstores import InMemoryVectorStore
import os
import dotenv
dotenv.load_dotenv()
os.environ["DASHSCOPE_API_KEY"]=os.getenv("MY_QIANWEN_KEY")

#大模型
llm=Tongyi(
    model="qwen-max"
)
#嵌入模型
emb=DashScopeEmbeddings(model="text-embedding-v4")
vector_stores=InMemoryVectorStore(embedding=emb)
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
res=vector_stores.similarity_search(user_input,k=2)
reference_text="["
for doc in res:
    reference_text+=doc.page_content
reference_text+="]"
def print_prompt(prompt):
    print("-" * 20)
    print(prompt.to_string())
    print("-"*20)
    return prompt
chain=prompt|print_prompt|llm|StrOutputParser()

response=chain.invoke({"question":user_input,"rag":reference_text})
print(response)