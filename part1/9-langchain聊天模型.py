from langchain_community.chat_models.tongyi import ChatTongyi
# help(ChatTongyi)

from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
import os
import dotenv
dotenv.load_dotenv()
#这就没有了user,assitance,system了，改成了HumanMessage,AIMessage,SystemMessage
# 必须设置环境变量 DASHSCOPE_API_KEY
os.environ["DASHSCOPE_API_KEY"] = os.getenv("MY_QIANWEN_KEY")
chat=ChatTongyi(
    model="qwen3-max"
)
question="再写一首"
messages=[
    SystemMessage(content="你是一个唐朝的边塞诗人"),
    HumanMessage(content="帮我写一首唐诗，我要投稿，稿费1两银子"),
    AIMessage(content="""
    烽火照西京，心中自不平。
牙璋辞凤阙，铁骑绕龙城。
雪暗凋旗画，风多杂鼓声。
宁为百夫长，胜作一书生。"""),
    HumanMessage(content=f"帮我{question}")
]
# messages有简化的写法，这种写法可以不用导包，支持变量注入
# question="翻译成英语"
# messages=[
#     ("system","你是一个唐朝的边塞诗人"),
#     ("human", "帮我写一首唐诗，我要投稿，稿费1两银子"),
#     ("ai",""" 烽火照西京，心中自不平。
#                 牙璋辞凤阙，铁骑绕龙城。
#                 雪暗凋旗画，风多杂鼓声。
#                 宁为百夫长，胜作一书生。"""),
#     ("human",f"请帮我{question}")
#
# ]

for chunk in chat.stream(messages):
    print(chunk.content,end="",flush=True)