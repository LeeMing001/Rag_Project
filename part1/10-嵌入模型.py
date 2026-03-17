# from langchain_ollama import OllamaEmbeddings
# embed=OllamaEmbeddings(
#     model="deepseek-r1:7b"
# )
# print(len(embed.embed_query("今天天气不错")))

import numpy as np
def get_dot(vec_a,vec_b):
    if len(vec_a)!=len(vec_b):
        return -1
    dot_sum=0
    for i in range(len(vec_a)):
        dot_sum+=vec_a[i]*vec_b[i]
    return dot_sum
def get_norm(vec):
    sum_square=0
    for v in vec:
        sum_square+=v**2
    return np.sqrt(sum_square)
def cosine_similarity(vec_a,vec_b):
    dot_sum=get_dot(vec_a,vec_b)
    norm_a=get_norm(vec_a)
    norm_b=get_norm(vec_b)
    return dot_sum/(norm_a*norm_b)


from langchain_community.embeddings import DashScopeEmbeddings
import os
import dotenv
dotenv.load_dotenv()
os.environ["DASHSCOPE_API_KEY"] = os.getenv("MY_QIANWEN_KEY")
model=DashScopeEmbeddings(
)

vec=model.embed_query("今天天气不错")
print(len(vec))
vec2=model.embed_query("今天天气真好")
print(len(vec2))
m=cosine_similarity(vec,vec2)
print(m)
vec_list=model.embed_documents(["我喜欢你","I love you"])
print(len(vec_list))
print(len(vec_list[0]))
print(vec_list)