# from langchain_community.llms.tongyi import Tongyi
# import os
# import dotenv
# dotenv.load_dotenv()
# os.environ["DASHSCOPE_API_KEY"]=os.getenv("MY_QIANWEN_KEY")
# llm=Tongyi(
#     model="qwen3.5-flash",
# )
# response=llm.invoke(input="你是谁")
# print(response)
# import dashscope
# import os
# import dotenv
# dotenv.load_dotenv()
#
# dashscope.api_key = os.getenv("MY_QIANWEN_KEY")
#
# response = dashscope.Generation.call(
#     model="qwen-max",
#     messages=[{"role": "user", "content": "你是谁"}]
# )
#
# if response.status_code == 200:
#     print(response.output.text)
# else:
#     print(f"Error: {response.code} - {response.message}")


from langchain_community.llms.tongyi import Tongyi
import os
import dotenv
dotenv.load_dotenv()

# 必须设置环境变量 DASHSCOPE_API_KEY
os.environ["DASHSCOPE_API_KEY"] = os.getenv("MY_QIANWEN_KEY")

llm = Tongyi(
    model="qwen-max",
)

response = llm.stream("你是什么模型")

for chunk in response:
    print(chunk, flush=True)#立即刷新



