##streamlit app 
import streamlit as st
import uuid
import requests
import time
BASE_URL = st.secrets["BASE_URL"]

def stream_generator(message):
    for word in message.split():
        yield word + " "
        time.sleep(0.002)

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
# user_query = st.chat_input("Say something")

for message in messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if user_query := st.chat_input(f"Write you queries regarding IR Code 2020."):
    st.session_state.messages.append({"role":"user", "content":user_query})
    response_post = requests.post(f"{BASE_URL}post_request?state_id={state_id}", json=messages)
    post_result = response_post.json().get("status")

    with st.chat_message("user"):
        st.markdown(f"{user_query}")    

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            if not post_result == "ok":
                st.markdown(f"Oh No! Server seems down for a while!🫨")

            response_get = requests.get(f"{BASE_URL}generate?user_query={user_query}&state_id={state_id}")
            query_result = response_get.json().get("message", "")

        if not query_result:
            st.markdown(f"Oh No! Server seems down for a while!🫨")

        st.markdown(query_result)
    
    st.session_state.messages.append({"role":"assistant", "content":query_result})

# if user_query:
#     with st.spinner("Getting your query sorted..."):
#         st.session_state.messages.append({"role":"user", "content":user_query})
#         response_post = requests.post(f"{BASE_URL}post_request?state_id={state_id}", json=messages)
#         response = requests.get(f"{BASE_URL}generate?user_query={user_query}&state_id={state_id}")
#         user_result = response.json()
#         st.session_state.messages.append({"role":"assistant", "content":user_result["message"]})
#         print(st.session_state.messages)
        
#     st.subheader("  ")
#     st.write(user_result["message"])