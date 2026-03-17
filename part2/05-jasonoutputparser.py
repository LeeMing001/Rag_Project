from langchain_core.prompts import ChatPromptTemplate
from langchain_core.prompts import MessagesPlaceholder
from langchain_community.chat_models.tongyi import ChatTongyi
import os
import dotenv
from langchain_core.output_parsers import StrOutputParser,JsonOutputParser

parser=StrOutputParser()
parser_json=JsonOutputParser()
dotenv.load_dotenv()

os.environ["DASHSCOPE_API_KEY"] = os.getenv("MY_QIANWEN_KEY")
chat_llm=ChatTongyi(
    model="qwen-max"
)
first_pormpt_template=ChatPromptTemplate.from_messages([
    ("system","你是一个擅长用诗经取名字的文学家"),
    ("human","请给我的邻居{lastname}先生的{gender}取个名字,你以json格式输出，key是name,value是刚起的名字")
])
second_prompt_template=ChatPromptTemplate.from_template(
    "姓名{name},请帮我解析含义"
)
chain=first_pormpt_template|chat_llm|parser_json|second_prompt_template|chat_llm|parser
res=chain.stream(input={"lastname":"王","gender":"女儿"})
# print(res)
for chunk in res:
    print(chunk,end="",flush=True)
# chain=first_pormpt_template|chat_llm|parser_json
# res=chain.invoke(input={"lastname":"王","gender":"女儿"})
# print(res)
# print(type(res))

