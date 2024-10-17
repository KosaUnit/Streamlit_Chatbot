import streamlit as st
import os
from dotenv import load_dotenv
from openai import AzureOpenAI

load_dotenv()

AZURE_OPENAI_API_ENDPOINT = os.getenv("AZURE_OPENAI_API_ENDPOINT")
AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY")
AZURE_OPENAI_API_VERSION = os.getenv("AZURE_OPENAI_API_VERSION")
AZURE_GPT_DEPLOYMENT_NAME = os.getenv("AZURE_GPT_DEPLOYMENT_NAME")

client = AzureOpenAI(
  azure_endpoint=AZURE_OPENAI_API_ENDPOINT, 
  api_key=AZURE_OPENAI_API_KEY,  
  api_version=AZURE_OPENAI_API_VERSION
)

st.title("Hi, my name is Cook!")
st.write("I'm your cooking assistant who can support you in your cooking jurney!")
st.write("You can ask me anything you want about cooking :)")

# conversation=[{"role": "system", "content": "You are a cooking assistant is a large language model trained by OpenAI. You can only response to the food related questions."}]

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = AZURE_GPT_DEPLOYMENT_NAME

if "conversation" not in st.session_state:
    st.session_state["conversation"] = [{"role": "system", "content": "You are a cooking assistant is a large language model trained by OpenAI. You can only response to the food related questions."}]

# Display chat messages from history on app rerun
for message in st.session_state["conversation"][1:]:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input(""):
    st.session_state["conversation"].append({"role": "user", "content": prompt})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)

    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        
        response = client.chat.completions.create(
            model=AZURE_GPT_DEPLOYMENT_NAME, # model = "deployment_name".
            messages=st.session_state["conversation"]
            )

        st.session_state["conversation"].append({"role": "assistant", "content": response.choices[0].message.content})
        st.markdown(st.session_state["conversation"][-1]["content"])

# Add a button to clean a conversation ...

if st.button('Clean Chat History'):
    for key in st.session_state.keys():
        del st.session_state[key]