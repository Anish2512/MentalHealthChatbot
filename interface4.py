import streamlit as st
import time
import requests
import voicetotext

# Add custom CSS for improved UI
def add_custom_css():
    st.markdown("""<style>
        body {
            background: linear-gradient(135deg, #f2f2f2 0%, #cce0ff 100%);
            font-family: 'Poppins', sans-serif;
            color: #333;
        }
        .stApp {
            padding: 0;
        }
        .css-1v3fvcr {
            padding-top: 0 !important;
        }
        .chat-interface {
            background-color: rgba(255, 255, 255, 0.8);
            border-radius: 15px;
            padding: 20px;
            box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.1);
            animation: slide-in 0.5s ease-out;
        }
        @keyframes slide-in {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }
        .message-container {
            display: flex;
            align-items: flex-start;
            margin-bottom: 10px;
        }
        .message-user {
            background-color: #007bff;
            color: white;
            border-radius: 20px;
            padding: 10px;
            max-width: 60%;
            animation: fade-in 0.5s ease-in-out;
        }
        .message-assistant {
            background-color: #f2f2f2;
            color: #333;
            border-radius: 20px;
            padding: 10px;
            max-width: 60%;
            animation: fade-in 0.5s ease-in-out;
        }
        @keyframes fade-in {
            from { opacity: 0; }
            to { opacity: 1; }
        }
        .follow-up {
            font-size: 18px;
            font-weight: 600;
            margin-top: 20px;
            animation: followup-appear 1s ease-in-out;
        }
        @keyframes followup-appear {
            from { opacity: 0; transform: scale(0.9); }
            to { opacity: 1; transform: scale(1); }
        }
        .personalized-greeting {
            font-size: 24px;
            font-weight: bold;
            animation: greeting-slide 1s ease-in-out;
            margin-top: 20px;
            margin-bottom: 20px;
        }
        @keyframes greeting-slide {
            from { transform: translateX(-50px); opacity: 0; }
            to { transform: translateX(0); opacity: 1; }
        }
        .stRadio > div {
            display: flex;
            justify-content: space-between;
        }
        .stButton > button {
            background-color: #007bff;
            color: white;
            border-radius: 12px;
            padding: 10px 20px;
            transition: all 0.3s ease;
        }
        .stButton > button:hover {
            background-color: #0056b3;
        }
        .flag-button {
            margin-top: 10px;
            width: 100%;
            background-color: #dc3545; /* Red */
        }
    </style>""", unsafe_allow_html=True)

def generate_response(message, value):
    new_data = {
        "Question": message,
        "User_Name": st.session_state.user_name,
        "User_Phone": st.session_state.user_phone,
        "Pincode": st.session_state.pincode,
        "Language": st.session_state.language
    }
    url_post = "http://localhost:8088/askquery" if value == 0 else "http://localhost:8088/askvector"
    post_response = requests.post(url_post, json=new_data)
    response_json = post_response.json()
    return response_json

def msendpin(pincode):
    new_data = {
        "Pincode": st.session_state.pincode
    }
    url_post = "http://localhost:8088/maps"
    post_response = requests.post(url_post, json=new_data)
    response_json = post_response.json()
    return response_json

def senddetail(user_name, user_phone, pincode, language):
    new_data = {
        "User_Name": user_name,
        "User_Phone": user_phone,
        "Pincode": pincode,
        "Language": language
    }
    url_post = "http://localhost:8088/askd"
    post_response = requests.post(url_post, json=new_data)
    response_json = post_response.json()
    return response_json

def getdetail():
    user_name = st.text_input("Enter your Name: ", type="default")
    user_phone = st.text_input("Enter your phone number: ", type="default")
    user_email = st.text_input("Enter your email: ", type="default")
    pincode = st.text_input("Enter your pincode: ", type="default")
    language = st.selectbox("Select a language...", ("English", "Hindi", "Kannada", "Tamil"))

    if st.button("Submit", icon="✅"):
        if user_name and user_phone and pincode and language:
            response = senddetail(user_name, user_phone, pincode, language)
            if response['status'] == 1:
                st.success("Successfully sent data")
            else:
                st.error("Error in sending data")
        else:
            st.error("Please enter all the details")
    return user_name, user_phone, pincode, language

def createside():
    with st.sidebar:
        v1 = st.checkbox("Search Trusted Sources")
        if v1 not in st.session_state:
            st.session_state.v1 = v1
        st.session_state.img = "./assets/red.png" if not st.session_state.v1 else "./assets/blue.png"
        pages = ["User info", "Chat", "Services"]
        page = st.radio("Select a page:", pages)
        return page

def services_page():
    maps = st.button("Find nearest hospitals", icon="🏥")
    if maps:
        hospital_info = msendpin(st.session_state.pincode)
        st.markdown("<h3>Hospital 1 details</h3>", unsafe_allow_html=True)
        st.markdown("Name: " + hospital_info['data']['hospital1'][0])
        st.markdown("Address: " + hospital_info['data']['hospital1'][1] + " Phone Number: " + hospital_info['data']['hospital1'][2])
        st.markdown("<h3>Hospital 2 details</h3>", unsafe_allow_html=True)
        st.markdown("Name: " + hospital_info['data']['hospital2'][0])
        st.markdown("Address: " + hospital_info['data']['hospital2'][1] + " Phone Number: " + hospital_info['data']['hospital2'][2])
        st.markdown("<h3>Hospital 3 details</h3>", unsafe_allow_html=True)
        st.markdown("Name: " + hospital_info['data']['hospital3'][0])
        st.markdown("Address: " + hospital_info['data']['hospital3'][1] + " Phone Number: " + hospital_info['data']['hospital3'][2])
    if st.button("Book a session", icon="📅"):
        sendm()
        st.success("Successfully booked a session, please check your email for further details")

def sendm():
    new_data = {
        "User_name": st.session_state.user_name,
    }
    url_post = "http://localhost:8088/maill"
    requests.post(url_post, json=new_data)

def sendinput(question, avatar):
    with st.chat_message("user", avatar=st.session_state.userimg):
        st.markdown(question)
    st.session_state.messages.append({"role": "user", "content": question, "avatar": st.session_state.userimg})
    response = generate_response(question, int(st.session_state.v1))
    answer = response['data']['Answer']
    full_response = ""
    with st.chat_message("assistant", avatar=avatar):
        message_placeholder = st.empty()
        for chunk in answer.split():
            full_response += chunk + " "
            time.sleep(0.05)
            message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown(full_response)
    if response['data']['Source1'] != "":
        st.info(response['data']['Source1'])
        st.info(response['data']['Source2'])
    follow = response['data']['Followup']
    st.markdown(f"<div class='follow-up'>Follow up question: {follow}</div>", unsafe_allow_html=True)
    st.session_state.messages.append({"role": "assistant", "content": answer, "avatar": st.session_state.img})

def chat_page():
    if "messages" not in st.session_state:
        st.session_state.messages = []
        st.session_state.v1 = 0

    for message in st.session_state.messages:
        with st.chat_message(message["role"], avatar=message["avatar"]):
            st.markdown(message["content"])

    # User input
    with st.container():
        st.text_input("Type your message:", key="input", on_change=sendinput, args=(st.session_state.input, st.session_state.img))
        st.button("Speak", on_click=sendinput, args=(voicetotext.voicetotext(), st.session_state.img))  # Button for voice input
        st.button("Flag Content", on_click=flag_content, args=(st.session_state.messages[-1],))  # Button to flag content

def flag_content(message):
    if "flagged_messages" not in st.session_state:
        st.session_state.flagged_messages = []
    st.session_state.flagged_messages.append(message)
    st.success("Message flagged successfully.")

def main():
    add_custom_css()
    st.title("InnerVerse - Your Mental Health Assistant")
    page = createside()
    if page == "User info":
        st.header("User Information")
        st.session_state.user_name, st.session_state.user_phone, st.session_state.pincode, st.session_state.language = getdetail()
    elif page == "Chat":
        st.header("Chat with your Assistant")
        chat_page()
    elif page == "Services":
        st.header("Services")
        services_page()

if __name__ == "__main__":
    main()
