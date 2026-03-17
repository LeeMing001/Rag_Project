#获取客户端对象
from openai import OpenAI
import os
import dotenv
dotenv.load_dotenv()
os.environ['OPENAI_BASE_URL']=os.getenv('GUIJI_BASE_URL')
os.environ['OPENAI_API_KEY']=os.getenv('MY_GUIJI_KEY')
client=OpenAI()
response=client.chat.completions.create(
    model="Pro/deepseek-ai/DeepSeek-V3.2",
    messages=[
        {"role":"system","content":"你是个AI工具"},
        # {"role":"assistant","content":"你对客户非常热情"},
        {"role":"user","content":"""
        请抽取产品名称和核心卖点两个字段，格式为Json，我提供两个示例
        *示例1：MacBook高效节能，性能强大，适合牛马使用，输出{"产品名称":"MacBook","产品卖点":"高效节能，性能强大"}；
        *示例2：联想笔记本拥有RTX4060独立显卡，玩游戏丝滑流畅，输出{"产品名称":"联想笔记本","产品卖点":"RTX4060独立显卡，丝滑流畅"}；
        请处理：华为MatepadPro，高清大屏，长效续航，你的好帮手
        """}
    ], 
    stream=True
)
# print(response.choices[0].message.content)
for chunk in response:
    content=chunk.choices[0].delta.content
    if content is not None:
        print(chunk.choices[0].delta.content,
          end="",#每一段之间以空格分割
          flush=True  #立刻刷新缓冲区
)
#调用模型
#处理结果