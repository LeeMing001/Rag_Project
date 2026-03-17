from openai import OpenAI
import os
import dotenv

dotenv.load_dotenv()

os.environ['OPENAI_API_KEY']=os.getenv('MY_GUIJI_KEY')
os.environ['OPENAI_BASE_URL']=os.getenv('GUIJI_BASE_URL')

client=OpenAI(
)
response=client.chat.completions.create(
    model="Pro/deepseek-ai/DeepSeek-V3.2",
    messages=[
        {"role":"system","content":"你是AI助手"},
        {"role":"assistant","content":"你是个高冷的美女"},
        {"role":"user","content":"小明有3只狗"},
        {"role":"assistant","content":"好的"},
        {"role":"user","content":"晓莉有2只猫"},
        {"role":"assistant","content":"好的"},
        {"role":"user","content":"一共有几只宠物"}
    ],
    stream=True
)
for chunk in response:
    content=chunk.choices[0].delta.content
    if content is not None:
        print(
            chunk.choices[0].delta.content,
            end="",
            flush=True
        )

