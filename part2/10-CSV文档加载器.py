#文档加载器内部都实现了两个方法
#load()和lazy_load()一个是一次性加载全部文档，一个是延迟流式传输文档
from langchain_community.document_loaders import CSVLoader,JSONLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

loader=CSVLoader(file_path="./data.csv",
                 csv_args={"delimiter":",",
                           "quotechar":"'",
                           "fieldnames":['a','b','c',"d"]},
                 encoding="utf-8")
# docs=loader.load() #返回一个[Document,Document…]
# print(docs)
# documents=loader.load()
# for document in documents:
#     print(type( document), document)
for doc in loader.lazy_load():
    print(doc)

loader_json=JSONLoader(
    file_path="./data.json",#文件路径
    jq_schema=".name",#jq schema语法
    text_content=False,
    #抽取的是否是字符串，默认True
    json_lines=True,#是否是JsonLines格式,每一行都是json文件
)
res=loader_json.load()
print(res)
print(type(res))
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
loader=TextLoader(
    "./data.txt",
    encoding="utf-8"
)
docs=loader.load()
print(docs)
splitter=RecursiveCharacterTextSplitter(
    chunk_size=8, #分段最大字符数
    chunk_overlap=0, #分段之间允许重叠字符数
    separators=["\n\n","\n","\t"," ","?","!",".","。","？"],
    length_function=len,
)
split_docs=splitter.split_documents(docs)
print(len(split_docs))
i=0
for s in split_docs:
    i+=1
    print(f"第{i}段：",s)