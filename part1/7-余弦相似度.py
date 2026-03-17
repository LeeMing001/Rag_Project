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
A=[0.5,0.5]
B=[0.7,0.7]
C=[0.7,0.5]
D=[-0.6,-0.5]
print(cosine_similarity(A,B))
print(cosine_similarity(B,C))
print(cosine_similarity(B,D))



