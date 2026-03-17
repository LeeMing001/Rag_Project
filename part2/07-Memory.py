#基于RunnableWithMessageHistory在原有链的基础上创建带有历史记录功能的新链
#基于InMemoryChatMessageHistory为历史记录提供内存存储
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain_community.chat_models.tongyi import ChatTongyi
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.chat_history import InMemoryChatMessageHistory
import os
import dotenv
from Mem import FileChatMessageHistory
dotenv.load_dotenv()
os.environ["DASHSCOPE_API_KEY"] = os.getenv("MY_QIANWEN_KEY")
chat_llm=ChatTongyi(
    model="qwen-max"
)
# prompt=ChatPromptTemplate.from_template(
#     "你需要根据会话历史回应用户问题，会话历史问题{chat_history}，用户问题{question}，请回答"
#                                     )
prompt=ChatPromptTemplate.from_messages(
    [
        ("system","你需要根据历史会话回应用户问题，对话历史："),
        MessagesPlaceholder("chat_history"),
        ("human"," {question}")
    ]
)
str_parser=StrOutputParser()
def print_prompt(full_prompt):
    print("-"*20,full_prompt.to_string(),"-"*20)
    return full_prompt
chain=prompt|print_prompt|chat_llm|str_parser
# store={}
# def get_history(session_id):
#     if session_id not in store:
#         store[session_id]=InMemoryChatMessageHistory()
#     return store[session_id]
# 创建带有历史记录功能的新链,自动附加历史消息
def get_history(session_id):
    return FileChatMessageHistory(session_id,"./history")
conversation_chain=RunnableWithMessageHistory(
    chain,#被增强的原有链
    get_history,#获取历史消息的函数
    input_messages_key="question",#输入的问题的key
    history_messages_key="chat_history"#历史消息的key
)
if __name__=="__main__":
    session_config={
        "configurable":{
            "session_id":"123"
        }
    }
    session_config2 = {
        "configurable": {
            "session_id": "124"
        }
    }
    # res=conversation_chain.invoke({"question":"你好,我叫小米"},session_config)
    # print("first：",res)
    # res = conversation_chain.invoke(input={"question": "你好,我叫红豆，我有个妹妹红米"}, config=session_config2)
    # print("first2：", res)
    # res = conversation_chain.invoke(input={"question": "我家有几个孩子"}, config=session_config2)
    # print("second2：", res)
    # res = conversation_chain.invoke(input={"question": "我养了7条斑马鱼，10条金鱼"}, config=session_config)
    # print("second：", res)
    res = conversation_chain.invoke(input={"question": "我一共养了几条鱼"}, config=session_config)
    print("third：", res)
