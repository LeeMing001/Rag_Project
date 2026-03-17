from langchain_core.runnables import RunnableLambda
from langchain_community.chat_models.tongyi import ChatTongyi
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
import os
import dotenv
dotenv.load_dotenv()
os.environ["DASHSCOPE_API_KEY"] = os.getenv("MY_QIANWEN_KEY")
chat_llm=ChatTongyi(
    model="qwen-max"
)
str_parser=StrOutputParser()
my_func=RunnableLambda(lambda ai_message:{"name":ai_message.content})
#from_messages只能是ChatPromptTemplate,from_template都可以
first_prmpt=ChatPromptTemplate.from_messages(
    [
        ("system","你是一个擅长用诗经取名字的文学家"),
        ("human","请给我的邻居{lastname}先生的{gender}取个名字,只输出名字")
    ]
)
second_prompt=ChatPromptTemplate.from_template("请帮我解析{name}的含义")
chain=first_prmpt|chat_llm|(lambda ai_message:{"name":ai_message.content})|second_prompt|chat_llm|str_parser
res=chain.invoke(input={"lastname":"王","gender":"女儿"})
print(res)