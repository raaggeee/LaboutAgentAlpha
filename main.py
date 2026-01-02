##streamlit app 
import streamlit as st
import uuid
import requests
import time
import authlib

BASE_URL = st.secrets["BASE_URL"]

if not st.user.is_logged_in:
    st.header("_Labour_:blue[Agent]")
    st.write("Still juggling between multiple Labour Law Websites and Documents?🫨")
    st.write("Try LabourAgent. Your one stop Labour Law guide.")
    st.subheader("What is LabourAgent?")
    st.write("LabourAgent is a Labour Law :blue[Agent]. It is an interactive way to know and apply Labour Law.")
    st.write("It is a one stop :blue[Agent] which provides:")
    st.markdown("- New and Updated Labour Law knowledge base.")
    st.markdown("- All Acts, Laws, Notifications and Rule related to Central and State Labour Laws.")
    st.markdown("- Interactive way to understand and apply Labour Laws in Corporate.")

    if st.button("Login with Google"):
        st.login("google")

    st.stop()


def stream_generator(message):
    for word in message.split():
        yield word + " "
        time.sleep(0.002)

if "uid" not in st.session_state:
    st.session_state.uid = str(uuid.uuid4())

if "messages" not in st.session_state:
    st.session_state.messages = []

if "curr_code" not in st.session_state:
    st.session_state.curr_code = ""

if "limit" not in st.session_state:
    st.session_state.limit = 0

state_id = st.user.email
messages = st.session_state.messages
# print(state_id)
data = {}
for k in ["is_logged_in", "given_name", "email", "email_verified"]:
    data[k] = st.user.get(k)

response_login = requests.post(f"{BASE_URL}login", json=[data])
#set limit
user_count = response_login.json().get("message", "")
count = user_count
st.session_state.limit = count


config = {"configurable": {"thread_id": state_id}}


st.header("_Labour_:blue[Agent]")
# user_input = st.text_input(label="Enter your query")
# user_query = st.chat_input("Say something")

for message in messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if st.session_state.limit != 10:
    if user_query := st.chat_input(f"Write you queries Labour Laws..."):
        
        st.session_state.messages.append({"role":"user", "content":user_query})

        with st.chat_message("user"):
            st.markdown(f"{user_query}")    

        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):

                response = requests.post(f"{BASE_URL}chat?state_id", json={"state_id": state_id, "messages":messages, "question": user_query})
                query_result = response.json().get("message", "")

            if not query_result:
                st.markdown(f"Oh No! Server seems down for a while!🫨")

            st.markdown(query_result)
        
        st.session_state.messages.append({"role":"assistant", "content":query_result})
        count += 1
        st.session_state.limit = count
else:
    feedback = {}
    with st.form("Feedback_Form"):
        st.write("Thanks for the conversation.")
        name = st.text_input("First Name")
        phone_no = st.text_input
        
option = st.selectbox(
            "For Code specific answer",
            ("Introduction to Labour Codes", "The Industry Relation Codes, 2020", "The Codes on Social Security, 2020", "The Codes on Wages, 2019", "The Occupation, Safety, Health and Working Condition Code, 2020"),
            placeholder="Select a Labour Law Code..."
            
        )

send_settings = requests.post(f"{BASE_URL}send_settings?state_id={state_id}&conversation_code={option}")
#for logout
st.button("Log out", on_click=st.logout)

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