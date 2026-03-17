from langchain_classic.chains.summarize.map_reduce_prompt import prompt_template
from langchain_core.messages import AIMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.prompts import MessagesPlaceholder
from langchain_community.chat_models.tongyi import ChatTongyi
import os
import dotenv
from langchain_core.output_parsers import StrOutputParser

parser=StrOutputParser()
dotenv.load_dotenv()

os.environ["DASHSCOPE_API_KEY"] = os.getenv("MY_QIANWEN_KEY")

chat_prompt=ChatPromptTemplate.from_messages([
    ("system","你是一个擅长用诗经取名字的文学家"),
    ("human","请给我的邻居{lastname}先生的{gender}取个名字")
])
llm=ChatTongyi(
    model="qwen-max"
)
second_prompt=ChatPromptTemplate.from_template("请解释这些名字的含义{names}")

# chain=chat_prompt|llm|parser|prompt_template|llm
# for chunk in chain.stream(input={"lastname":"王","gender":"女儿"}):
#     print(chunk.content,end="",flush=True)

chain=chat_prompt|llm|parser|second_prompt|llm|parser
res:str=chain.invoke({"lastname":"王","gender":"女儿"})
print(res)
print(type(res))