from langchain_community.document_loaders import PyPDFLoader

loader=PyPDFLoader(
    file_path="./20293_EcoPrune Non-Linear Sparsity Mapping via Entropy-Guided Sensitivity for LLM Pruning_1_13_translate_20260306221044.pdf",
    mode="page",
    password="123456",
)
i=0
for doc in loader.lazy_load():
    i+=1
    print(doc)
    print("-"*20)