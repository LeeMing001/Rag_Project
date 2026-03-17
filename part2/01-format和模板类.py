from langchain_community.llms.tongyi import Tongyi
from langchain_core.messages import AIMessage,HumanMessage,SystemMessage
from langchain_core.prompts import (PromptTemplate,
                                    FewShotPromptTemplate,
                                    ChatPromptTemplate)#这3个都是模板类
import os
import dotenv
dotenv.load_dotenv()
os.environ["DASHSCOPE_API_KEY"] = os.getenv("MY_QIANWEN_KEY")

llm=Tongyi(
    model="qwen-max"
)
prompt_template=PromptTemplate.from_template("我的邻居是{name},他喜欢{hobby}")
t=prompt_template.format(name="王先生",hobby="钓鱼")
print(t)
print(type(t))

res=prompt_template.invoke({"name":"王先生","hobby":"钓鱼"})
print(res)
print(type(res))
#他们的区别在于，PromptTemplate是单轮次，FewShotPPromptTemplate是给出示例
# ChatPromptTemplate是多轮次
