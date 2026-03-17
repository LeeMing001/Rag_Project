from langchain_core.prompts import ChatPromptTemplate
from langchain_core.prompts import MessagesPlaceholder
from langchain_community.chat_models.tongyi import ChatTongyi
import os
import dotenv
dotenv.load_dotenv()

os.environ["DASHSCOPE_API_KEY"] = os.getenv("MY_QIANWEN_KEY")

chat_prompt=ChatPromptTemplate.from_messages([
    ("system","你是一个唐朝边塞诗人"),
    MessagesPlaceholder("history"),
    ("human","{question}")
])
llm=ChatTongyi(
    model="qwen-max"
)
history_data=[
    ("human","给我写一首诗"),
    ("ai","窗前明月光，疑是地上霜"),
    ("human","好诗，请再来一首"),
    ("ai","锄禾日当午，汗滴禾下土")
]

chain=chat_prompt|llm
# response=chain.stream(input={"history":history_data,"question":"请给我写一首诗"})
for chunk in chain.stream(input={"history":history_data,"question":"请给我写一首诗"}):
    print(chunk.content,end="",flush=True)