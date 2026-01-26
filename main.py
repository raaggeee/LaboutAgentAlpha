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
        time.sleep(0.1)

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

response_login = requests.post(f"{BASE_URL}login")
#set limit
user_count = response_login.json().get("message", "")
st.session_state.limit = user_count


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

# if st.session_state.limit == 10:
#     feedback = {}
#     with st.form("Feedback_Form"):
#         st.write("Thanks for the conversation.")
#         name = st.text_input("First Name")
#         phone_no = st.text_input

option_type = st.selectbox(
    "Select Establishment type",
    ("Factory/Industry", "Shop and Commercial Establishments"),
    placeholder="Select Industry Type"
)

option_law_type = "Rules"

if option_type == "Factory/Industry":
    option_codes = st.selectbox(
                "For Code specific answer",
                ("Introduction to Labour Codes", "The Industry Relation Codes, 2020", "The Codes on Social Security, 2020", "The Codes on Wages, 2019", "The Occupation, Safety, Health and Working Condition Code, 2020", "The Employee Provident Funds Scheme, 1952", "The Employee State Insurance Act, 1948", "The Sexual Harassment of Women at Workplace Act, 2013"),
                placeholder="Select a Labour Law Code..."
                
    )


    if option_codes == "Labour Welfare Rules":
        option_states = st.selectbox(
            "For State specific answer",
            ("Delhi", "Haryana","Uttar Pradesh"),
            placeholder="Select a State..."
            
        )

    elif option_codes == "Introduction to Labour Codes":
        option_law_type = "Codes"
        option_states = "Central"

    elif option_codes == "The Codes on Wages, 2019":
        option_states = st.selectbox(
            "For State specific answer",
            ("Central", "Delhi", "Haryana", "Uttar Pradesh"),
            placeholder="Select a State..."
        )

        if option_states == "Central":
            option_law_type = "Codes"

    elif (option_codes == "The Sexual Harassment of Women at Workplace Act, 2013" or option_codes == "The Employee Provident Funds Scheme, 1952" or option_codes == "The Employee State Insurance Act, 1948"):
        option_law_type = "Codes"
        option_states = "Central"

    elif option_codes == "The Industry Relation Codes, 2020":
        option_states = st.selectbox(
            "For State specific answer",
            ("Central", "Haryana"),
            placeholder="Select a State..."
        )
        if option_states == "Central":
            option_law_type = "Codes"

    elif option_codes == "The Occupation, Safety, Health and Working Condition Code, 2020":
        option_states = st.selectbox(
            "For State specific answer",
            ("Central", "Haryana", "Uttar Pradesh"),
            placeholder="Select a State..."
        )
        if option_states == "Central":
            option_law_type = "Codes"

    else:
        option_states = st.selectbox(
            "For State specific answer",
            ("Central", "Delhi", "Haryana", "Uttar Pradesh"),
            placeholder="Select a State..."
            
        )
        

        if option_states == "Central" and option_codes != "Introduction to Labour Codes":
            option_law_type = "Codes"


        if option_codes == "Introduction to Labour Codes":
            option_law_type = "Codes"

        else:
            option_law_type = "Rules"
    
    option_json = {
        "state_id": state_id,
        "conversation_code": option_codes,
        "india_state": option_states,
        "estb_type": "factory",
        "law_type": option_law_type
    }

else:
    option_states = st.selectbox(
        "For State specific answer",
        ("Haryana"),
        placeholder="Select a State..."
    )

    option_codes = "None"

    if option_states == "Central":
        option_codes = "The Employee State Insurance Act, 1948"
        option_codes = st.selectbox("For Central Provisions", ("The Employee State Insurance Act, 1948", "The Employee Provident Funds Scheme, 1952"), placeholder="Select Respective Provisions...", disabled=True)

    if option_states == "Haryana":
        option_codes = "Shops and Commercial Establishments"
        option_codes = st.selectbox("For State Provisions", ("Shops and Commercial Establishments"), placeholder="Select Respective Provisions...")

    option_json = {
        "state_id": state_id,
        "india_state": option_states,
        "conversation_code": option_codes,
        "estb_type":"shop_and_comm_estd",
        "law_type":""
    }

st.button("Log out", on_click=st.logout)
if st.button("💬 Give feedback"):
    st.session_state.show_form = True

# Feedback form (conditionally rendered)
if st.button("💬 Give feedback"):
    st.session_state.show_form = True

if st.session_state.get("show_form"):
    with st.form("feedback_form"):

        # Q1: Overall rating
        overall = st.radio(
            "⭐ Overall experience",
            ["⭐", "⭐⭐", "⭐⭐⭐", "⭐⭐⭐⭐", "⭐⭐⭐⭐⭐"],
            horizontal=True
        )

        # Q2: Relevance
        relevance = st.radio(
            "⭐ Were the answers relevant?",
            ["⭐", "⭐⭐", "⭐⭐⭐", "⭐⭐⭐⭐", "⭐⭐⭐⭐⭐"],
            horizontal=True
        )

        # Q3: Helpfulness
        helpfulness = st.radio(
            "⭐ Was it helpful?",
            ["⭐", "⭐⭐", "⭐⭐⭐", "⭐⭐⭐⭐", "⭐⭐⭐⭐⭐"],
            horizontal=True
        )

        feedback = st.text_area(
            "Additional comments (optional)",
            placeholder="Tell us what could be better…"
        )

        col1, col2 = st.columns(2)
        with col1:
            submit = st.form_submit_button("Submit")
        with col2:
            cancel = st.form_submit_button("Cancel")

        if submit:
            st.success("Thanks for your feedback! ⭐")
            feedback_json = {
                "state_id":state_id,
                "rating": len(rating),
                "relevancy": len(relevance),
                "helfulness": len(helpfulness),
                "feedback": feedback
            }
            post_feedback = requests.post(f"{BASE_URL}send_feedback", json=feedback_json)
            st.session_state.show_form = False

        if cancel:
            st.session_state.show_form = False

send_settings = requests.post(f"{BASE_URL}send_settings", json=option_json)


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
