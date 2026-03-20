
from datetime import datetime
import config_data as config
import hashlib
from langchain_chroma import Chroma
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

import os
import dotenv
dotenv.load_dotenv()
os.environ["DASHSCOPE_API_KEY"]=os.getenv("MY_QIANWEN_KEY")

def check_md5(md5_str:str):
    """
    检查传入的md5字符串是否被处理过了
    :return: False表示未处理过，True表示处理过
    """
    if not os.path.exists(config.md5_path):
        #文件不存在的情况下肯定没处理过
        open(config.md5_path,"w",encoding="utf-8").close()
    else:
        for line in open(config.md5_path,"r",encoding="utf-8").readlines():
            line=line.strip() #处理字符串前后的空格
            if line == md5_str:
                return True
    return False

def save_md5(md5_str:str):
    """将传入的md5记录到文件中"""
    with open(config.md5_path,"a",encoding="utf-8") as f:
        f.write(md5_str+'\n')
def get_string_md5(input_str:str,encoding="utf-8"):
    """将传入的字符串转为md5字符串"""
    #将字符串转换为bytes字节数组
    str_bytes=input_str.encode(encoding=encoding)#将字符串转为二进制
    md5_obj=hashlib.md5()
    md5_obj.update(str_bytes)#传入要转换的二进制数据，大文件可以分多次转入，所以叫update
    md5_hex=md5_obj.hexdigest()#得到md5的十六进制字符串
    return md5_hex
class KnowledgeBaseService(object):
    def __init__(self):
        os.makedirs(config.persist_directory,exist_ok=True)
        self.chroma=Chroma(
            collection_name=config.collection_name,
            embedding_function=DashScopeEmbeddings(model="text-embedding-v4"),
            persist_directory=config.persist_directory
        )
        self.spliter=RecursiveCharacterTextSplitter(
            chunk_size=config.chunk_size,
            chunk_overlap=config.chunk_overlap,
            separators=config.separators,
            length_function=len,
        )
    def upload_by_str(self,data,filename):
        """将传入的字符串向量化，存入向量库中"""

        #先拿到传入字符串的md5值
        md5_hex=get_string_md5(data)
        #查询是否已经有了
        if check_md5(md5_hex):
            return '跳过'
        #先查看长度进行文本分割
        if len(data)>config.max_split_char_number:
            knowledge_chunks=self.spliter.split_text(data)
        else:
            knowledge_chunks=[data]
        metadata = {
            "source": filename,
            "create_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "operator": "liming"
        }

        self.chroma.add_texts( #内容加载到向量库中
            #iterable->str
            knowledge_chunks,
            metadatas=[metadata for _ in knowledge_chunks]
        )
        save_md5(md5_hex)
        return 'sucess'




if __name__=="__main__":
    service=KnowledgeBaseService()
    t=service.upload_by_str("周杰伦","textfile")
    print(t)