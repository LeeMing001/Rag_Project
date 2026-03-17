from langchain_core.prompts import PromptTemplate
from langchain_community.llms.tongyi import Tongyi
import os
import dotenv
dotenv.load_dotenv()
os.environ["DASHSCOPE_API_KEY"] = os.getenv("MY_QIANWEN_KEY")

prompt_template=PromptTemplate.from_template(
    "我的邻居姓{lastname},刚生了{gender}孩,你帮我起个名字，简单回答"
)
# prompt_text=prompt_template.format(lastname="王",gender="女")
# print(prompt_text)
llm=Tongyi(
    model="qwen-max"
)
# res=llm.invoke(input=prompt_text)
# print(res)
chain=prompt_template|llm
res=chain.invoke(input={"lastname":"王","gender":"女"})
print(res)

