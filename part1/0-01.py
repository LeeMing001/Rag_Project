from langchain_openai import ChatOpenAI
import dotenv
import os
dotenv.load_dotenv()
os.environ['OPENAI_API_KEY']=os.getenv('MY_QIANWEN_KEY')#这样写了以后就不用再给client传参了
os.environ['OPENAI_BASE_URL']=os.getenv('QIANWEN_BASE_URL')

client = ChatOpenAI(
    model="qwen3.5-flash",
)

response = client.invoke(
"你好，请问你是谁"
)
print(response)