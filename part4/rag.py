from langchain_community.embeddings import DashScopeEmbeddings
from langchain_openai.embeddings import OpenAIEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.documents import Document
import config_data as config
from part4.vector_store import VectorStoreService
from langchain_community.chat_models.tongyi import  ChatTongyi
from langchain_openai import OpenAI, ChatOpenAI
from langchain_core.output_parsers import StrOutputParser

import os
import dotenv
from langchain_core.documents import Document
dotenv.load_dotenv()
os.environ["OPENAI_BASE_URL"]=os.getenv("GUIJI_BASE_URL")
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
                ("system","你是一个AI助手，你的回答很简洁，请根据以下内容{rag}，回答用户问题"),
                ("human","{question}")
            ]
        )
        self.chat_model=ChatOpenAI(model=config.chat_model_name)
        self.chain=self.__get_chain()
    def __get_chain(self):
        """获取最终执行链"""
        retriver=self.vector_service.get_retriever()
        def format_document(docs:list[Document]):
            if not docs:
                return "无相关参考资料"
            formated_str = ""
            for doc in docs:
                formated_str += f"文档片段：{doc.page_content}\n文档元数据:{doc.metadata}\n"
            return formated_str
        chain = ({"question": RunnablePassthrough(),
                 "rag": retriver | format_document
                } | self.prompt_template | print_prompt|self.chat_model | StrOutputParser())
        return chain
if __name__=="__main__":
    service=RagService()
    res=service.chain.invoke("如何评价美的空调")
    print(res)