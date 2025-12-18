##streamlit app 
import streamlit as st
import uuid
import requests

if "uid" not in st.session_state:
    st.session_state.uid = str(uuid.uuid4())

state_id = st.session_state.uid
print(state_id)

config = {"configurable": {"thread_id": state_id}}


st.header("_Labour_:blue[Agent]")
user_input = st.text_input(label="Enter your query")

if st.button("Run"):
    with st.spinner("Getting your query sorted..."):
        response = requests.get(f"https://api.nodrik.com/app/generate?user_query={user_input}%21&state_id={state_id}")
        user_result = response.json()
        
    st.subheader("Explaination")
    st.write(user_result["message"])