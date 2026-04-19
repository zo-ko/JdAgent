import streamlit as st
from time import sleep
from rag import RagService
import config_data as config

st.title("智能客服")
st.divider()

rag_service = RagService()

if "rag" not in st.session_state:
    st.session_state["rag"] = rag_service

if "message" not in st.session_state:
    st.session_state["message"] = [{"role" : "assistant","content":"hello,how can I help you?"}]

for message in st.session_state["message"]:
    st.chat_message(message["role"]).write(message["content"])

prompt = st.chat_input()

if prompt:

    st.chat_message("user").write(prompt)
    st.session_state["message"].append({"role":"user","content":prompt})

    ai_res_list = []
    with st.spinner("思考中"):
        res = st.session_state["rag"].invoke(
            prompt,
            session_id = "koko"
        )

        def capture(generator,cache_list:list):
            for chunk in generator:
                cache_list.append(chunk)
                yield chunk

        st.chat_message("assistant").write_stream(capture(res,ai_res_list))
        st.session_state["message"].append({"role":"assistant","content":"".join(ai_res_list)})