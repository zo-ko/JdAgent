
from time import sleep
import streamlit as st
from knowledge_base import KnowledgeBaseService

st.title("知识库更新")

uploader_file = st.file_uploader(
    "上传文件", 
    type=["txt"],
    accept_multiple_files=False,
)

service = KnowledgeBaseService()
if "service" not in st.session_state:
    st.session_state["service"] = service

if uploader_file is not None:
    file_name = uploader_file.name
    file_type = uploader_file.type
    file_size = uploader_file.size/1024

    st.subheader(f"文件名: {file_name}")
    st.subheader(f"文件类型: {file_type}")
    st.subheader(f"文件大小: {file_size:.2f} KB")

    text= uploader_file.getvalue().decode("utf-8")
    st.text_area("文件内容", text, height=300)

    with st.spinner("正在上传到知识库..."): 
        sleep(1)  # 模拟上传过程中的等待时间
        res = st.session_state["service"].upload_by_str(text, file_name)
        st.write(res)