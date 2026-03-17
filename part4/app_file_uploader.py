"""
基于streamlit完成WEB网页上传服务
pip install streamlit
"""
import time

import streamlit as st
from knowledge_base import KnowledgeBaseService

#添加网页标题
st.title("知识库更新服务")
uploader_file=st.file_uploader(
    "请上传TXT文件",
    type=["TXT"],
    accept_multiple_files=False#仅接受一个文件的上传
)
if "service" not in st.session_state:
    st.session_state["service"]=KnowledgeBaseService()
if uploader_file is not None:
    file_name=uploader_file.name
    file_type=uploader_file.type
    file_size=uploader_file.size/1024 #得到kb单位
    st.subheader(f"文件名：{file_name}")
    st.write(f"格式：{file_type}|大小：{file_size:2f}kB")
    #get_value->bytes->decode()
    text=uploader_file.getvalue().decode("utf-8")
    with st.spinner("文件加载中"):
        time.sleep(1)
        res=st.session_state["service"].upload_by_str(text,file_name)
        st.write(res)

