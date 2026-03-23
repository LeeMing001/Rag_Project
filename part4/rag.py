from langchain_community.embeddings import DashScopeEmbeddings
from langchain_openai.embeddings import OpenAIEmbeddings
from langchain_core.prompts import ChatPromptTemplate,MessagesPlaceholder
from langchain_core.runnables import RunnablePassthrough, RunnableWithMessageHistory, RunnableLambda
from langchain_core.documents import Document
import config_data as config
from part4.vector_store import VectorStoreService
from langchain_openai import OpenAI, ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from file_history_store import get_history

import os
import dotenv
from langchain_core.documents import Document
dotenv.load_dotenv()
os.environ["OPENAI_API_BASE"]=os.getenv("GUIJI_BASE_URL")
os.environ["OPENAI_API_KEY"]=os.getenv("MY_GUIJI_KEY")
def print_prompt(prompt):
    print("-" * 20)
    print(prompt.to_string())
    print("-" * 20)
    return prompt

class RagService(object):
    def __init__(self):
        self.vector_service=VectorStoreService(
            embedding=OpenAIEmbeddings(model=config.embeddings_model_name)
        )
        self.prompt_template=ChatPromptTemplate.from_messages(
            [
                ("system","你是一个AI助手，你的回答很简洁，请根据以下内容{rag}，回答用户问题,历史记录如下"),
                MessagesPlaceholder("history"),
                ("human","{input}")
            ]
        )
        self.chat_model=ChatOpenAI(model=config.chat_model_name)
        self.chain=self.__get_chain()
    def __get_chain(self):
        """获取最终执行链"""
        retriever=self.vector_service.get_retriever()
        def format_document(docs:list[Document]):
            if not docs:
                return "无相关参考资料"
            formated_str = ""
            for doc in docs:
                formated_str += f"文档片段：{doc.page_content}\n文档元数据:{doc.metadata}\n"
            return formated_str
        # def format_for_retriever(value):
        #     print("----",value,"----")
        #     return value["input"]

        def format_for_retriever(value):
            # value 是包含 "input" 和 "history" 的字典
            current_input = value["input"]
            history_messages = value.get("history", [])

            # 将历史消息转换为字符串（这里假设历史消息是 LangChain 的 BaseMessage 对象列表）
            history_str = ""
            if history_messages:
                # 只取最近 N 条消息，避免查询过长（这里取最近 3 条）
                recent_history = history_messages[-3:]
                # 拼接消息内容
                history_str = " ".join([msg.content for msg in recent_history])

            # 组合查询：历史记录 + 当前问题
            query = f"{history_str} {current_input}".strip()
            return query
        def format_for_prompt_template( value):
            new_value={}
            new_value["input"]=value["input"]["input"]
            new_value["rag"]=value["rag"]
            new_value["history"] = value["input"]["history"]
            return new_value
        chain = ({"input": RunnablePassthrough(),
                 "rag": RunnableLambda(format_for_retriever)|retriever | format_document
                } | RunnableLambda(format_for_prompt_template)|self.prompt_template |print_prompt|self.chat_model | StrOutputParser())
        conversation_chain=RunnableWithMessageHistory(
             chain,
            get_history,
            input_messages_key="input",
            history_messages_key="history",
        )
        return conversation_chain

if __name__=="__main__":
    session_config = {
        "configurable": {
            "session_id": "123"
        }
    }
    service=RagService()
    res=service.chain.invoke({"input":"我穿不进去"},session_config)
    print(res)