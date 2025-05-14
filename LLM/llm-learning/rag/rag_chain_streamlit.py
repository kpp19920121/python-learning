import streamlit as st
import os,sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))



from ..langchain_llm.ollama import connect_ollama

st.title="动手学大模型开发"


def generate_response(message):


    print(f"开始对话:{message}")

    response=chatwithollama(message);



    print(f"返回的内容为:{response.message.content}")

    st.info({response.message.content})

with st.form('my_form'):
    text = st.text_area('Enter text:', 'What are the three key pieces of advice for learning how to code?')
    submitted = st.form_submit_button('Submit')

    if submitted :
        generate_response(text)

