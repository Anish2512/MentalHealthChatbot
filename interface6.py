import streamlit as st
import time
import requests
import voicetotext

# Add custom CSS for improved UI
def add_custom_css():
    st.markdown("""
        <style>
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

            /* Styling for user message */
            .message-user {
                background: linear-gradient(135deg, #6A82FB, #FC5C7D);
                color: white;
                border-radius: 20px;
                padding: 10px;
                max-width: 60%;
                margin-bottom: 10px;
                word-wrap: break-word;
                animation: fade-in 0.5s ease-in-out;
            }

            /* Styling for assistant message */
            .message-assistant {
                background-color: white;
                color: black;
                border-radius: 20px;
                padding: 10px;
                max-width: 60%;
                margin-bottom: 10px;
                word-wrap: break-word;
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
               /* InnerVerse Title aligned to the left */
            .innerverse-title {
                text-align: left;
                font-family: 'Poppins', sans-serif;
                font-weight: bold;
                font-size: 40px;
                background: linear-gradient(135deg, #6A82FB, #FC5C7D);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                letter-spacing: 2px;
                margin-bottom: 10px; /* Closer to tagline */
                margin-left: 0px; /* Aligned to the left */
                animation: title-slide 1s ease-out;
            }

            /* Tagline immediately below the title with minimal space */
            .innerverse-tagline {
                text-align: left;
                font-family: 'Poppins', sans-serif;
                font-size: 24px;  /* Slightly smaller size for balance */
                background: linear-gradient(135deg, #6A82FB, #FC5C7D);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                font-weight: 500;
                color: white;
                margin-top: 0px;   /* No extra space above tagline */
                margin-left: 0px;  /* Aligned to the left */
                animation: tagline-fade 1s ease-in-out;
            }

            /* Animation for the title and tagline */
            @keyframes title-slide {
                from { transform: translateY(-50px); opacity: 0; }
                to { transform: translateY(0); opacity: 1; }
            }
            @keyframes tagline-fade {
                from { opacity: 0; transform: translateY(20px); }
                to { opacity: 1; transform: translateY(0); }
            }

            /* Style for the name in personalized greeting */
            .personalized-name {
                background: linear-gradient(135deg, #6A82FB, #FC5C7D);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                font-weight: bold;
            }

            /* The greeting text should be white except the name */
            .personalized-greeting {
                font-size: 24px;
                font-family: 'Poppins', sans-serif;
                color: white; /* White text */
                margin-top: 20px;
                animation: greeting-slide 1s ease-in-out;
            }

            /* Animation for the greeting */
            @keyframes greeting-slide {
                from { transform: translateX(-50px); opacity: 0; }
                to { transform: translateX(0); opacity: 1; }
            }
                /* General chat styling */
            .chat-container {
                background-color: #000; /* Black background */
                padding: 20px;
                height: 500px;
                overflow-y: auto;  /* Scrollable if content exceeds */
                border-radius: 10px;
                box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
            }
        </style>
    """, unsafe_allow_html=True)

def generate_response(message, value):
    new_data = {
        "Question": message,
        "User_Name": st.session_state.user_name,
        "User_Phone": st.session_state.user_phone,
        "Pincode": st.session_state.pincode,
        "Language": st.session_state.language
    }
    if value == 0:
        url_post = "http://localhost:8088/askquery"
    else:
        url_post = "http://localhost:8088/askvector"
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
        if int(st.session_state.v1) == 0:
            st.session_state.img = "./assets/red.png"
        else:
            st.session_state.img = "./assets/blue.png"
        pages = ["User info", "Chat", "Services"]
        page = st.radio("Select a page:", pages)
        return page


def main():
    # Add custom CSS for better design
    add_custom_css()

    if 'messages' not in st.session_state:
        st.session_state.messages = []
        
    if 'user_name' not in st.session_state:
        st.session_state.user_name = ""
        
    st.title('InnerVerse')

    # Sidebar selection for pages
    page = createside()

    if page == "User info":
        user_name, user_phone, pincode, language = getdetail()
        if not st.session_state.user_name and user_name:
            st.session_state.user_name = user_name

    elif page == "Chat":
        st.header('InnerVerse Chat Interface')

        user_message = st.text_input("You:")
        if st.button('Send', key='send'):
            st.session_state.messages.append(('user', user_message))
            # Add your message generation logic here
            response = generate_response(user_message, 0)
            st.session_state.messages.append(('assistant', response))

        # Display the chat conversation with new CSS styles
        for role, message in st.session_state.messages:
            if role == 'user':
                st.markdown(f'<div class="message-container"><div class="message-user">{message}</div></div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="message-container"><div class="message-assistant">{message}</div></div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
