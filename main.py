##streamlit app 
import streamlit as st
import uuid
import requests
BASE_URL = st.secrets["BASE_URL"]

if "uid" not in st.session_state:
    st.session_state.uid = str(uuid.uuid4())

state_id = st.session_state.uid
print(state_id)

config = {"configurable": {"thread_id": state_id}}


st.header("_Labour_:blue[Agent]")
# user_input = st.text_input(label="Enter your query")
user_query = st.chat_input("Say something")

if user_query:
    with st.spinner("Getting your query sorted..."):
        response = requests.get(f"{BASE_URL}generate?user_query={user_query}%21&state_id={state_id}")
        user_result = response.json()
        
    st.subheader("  ")
    st.write(user_result["message"])