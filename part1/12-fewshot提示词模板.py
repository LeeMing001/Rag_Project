from langchain_core.prompts import FewShotPromptTemplate,PromptTemplate
from langchain_community.llms.tongyi import Tongyi
import os
import dotenv
dotenv.load_dotenv()
os.environ["DASHSCOPE_API_KEY"] = os.getenv("MY_QIANWEN_KEY")

prompt_template=PromptTemplate.from_template(
    "科目:{class},成绩:{score}"
)
examples_data=[
    {"class":"英语","score":90},
    {"class":"数学","score":99},
    {"class":"语文","score":115},
    {"class":"历史","score":46}
]#要求是list套字典
pre="以下是一个同学的成绩，语文、数学、英语满分120，其他科目满分50"

few_shot_template=FewShotPromptTemplate(
    example_prompt=prompt_template,#示例数据模板
    examples=examples_data,#示例数据
    prefix=pre,#示例前缀
    suffix="请推测这个同学的{class}成绩",#示例后缀
    input_variables=["class"]#前缀或后缀中需要输入的变量名
)
print(few_shot_template)
print(type(few_shot_template))
prompt_text=few_shot_template.invoke(input={"class":"政治"})
print(str(prompt_text))
print(type(str(prompt_text)))
# llm=Tongyi(
#     model="qwen-max"
# )
# chain=few_shot_template|llm
# res=chain.invoke(input={"class":"政治"})
# print(res)