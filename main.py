##streamlit app 
import streamlit as st
import uuid
import requests
BASE_URL = st.secrets["BASE_URL"]

if "uid" not in st.session_state:
    st.session_state.uid = str(uuid.uuid4())

if "messages" not in st.session_state:
    st.session_state.messages = []

state_id = st.session_state.uid
messages = st.session_state.messages
print(state_id)

config = {"configurable": {"thread_id": state_id}}


st.header("_Labour_:blue[Agent]")
# user_input = st.text_input(label="Enter your query")
user_query = st.chat_input("Say something")

if user_query:
    with st.spinner("Getting your query sorted..."):
        st.session_state.messages.append({"role":"user", "content":user_query})
        response_post = requests.post(f"{BASE_URL}post_request?state_id={state_id}", json=messages)
        response = requests.get(f"{BASE_URL}generate?user_query={user_query}&state_id={state_id}")
        user_result = response.json()
        st.session_state.messages.append({"role":"assistant", "content":user_result["message"]})
        print(st.session_state.messages)
        
    st.subheader("  ")
    st.write(user_result["message"])