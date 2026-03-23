"""
基于streamlit完成WEB网页上传服务
pip install streamlit
streamlit run app_file_uploader.py
"""
import time

import streamlit as st #前端
from knowledge_base import KnowledgeBaseService

#添加网页标题
st.title("知识库更新服务")
uploader_file=st.file_uploader(
    "请上传TXT文件",
    type=["TXT"],
    accept_multiple_files=False#仅接受一个文件的上传
)
if "service" not in st.session_state: #st.session_state是存储用户信息，
    st.session_state["service"]=KnowledgeBaseService()
#streamlit一个前端交互的库，每次点击都会全量更新，要保存内容需要通过session_state保存
#除非用户刷新页面，否则数据不会丢失
#用户上传数据，会自动重新运行整个脚本
if uploader_file is not None:
    file_name=uploader_file.name
    file_type=uploader_file.type
    file_size=uploader_file.size/1024 #得到kb单位
    st.subheader(f"文件名：{file_name}")#二级标题
    st.write(f"格式：{file_type}|大小：{file_size:.2f}kB") #普通大小文字
    #get_value->bytes->decode()
    text=uploader_file.getvalue().decode("utf-8")
    with st.spinner("文件加载中"):#创建spinner组件
        time.sleep(1)
        res=st.session_state["service"].upload_by_str(text,file_name)#从上传的文件中取出文本
        st.write(res)

