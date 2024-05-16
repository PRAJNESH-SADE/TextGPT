import streamlit as st
from dotenv import load_dotenv
load_dotenv()

import os
import cohere
from cohere.responses.chat import StreamEvent
# assuming .env file in parent dir exists
# with COHERE_API_KEY = your_api_key
co = cohere.Client(os.environ.get("COHERE_API_KEY"))

st.title("TextGpt")


# def response_generator():
#     responses = [
#         "Hello there! How can I assist you today?",
#         "I'm here to help. What do you need?",
#         "Hey! What can I do for you?",
#         "Hi! What do you need help with?"
#     ]
#     response = random.choice(responses)
#     for word in response.split():
#         yield word + " "
#         time.sleep(0.05)

def cohere_response_generator(prompt):
    chat_history = list(map(lambda x: {
        "user_name" : "User" if x["role"] == "user" else "Chatbot",
        "text" : x["content"]
    }, st.session_state.messages[-3:]))
    for event in co.chat(message = f" .{prompt}  ", chat_history = chat_history, stream = True):
    # for event in co.chat(message = prompt, chat_history = chat_history, stream = True):
        if event.event_type == StreamEvent.TEXT_GENERATION:
            yield event.text
        elif  event.event_type == StreamEvent.STREAM_END:
            return ""

#initialize a chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

#Display the chat messages from the chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Say something..."):
    #Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({ "role" : "user" , "content" : prompt })
    
    #Display the assistant response in chat message container
    with st.chat_message("assistant"):
        response = st.write_stream(cohere_response_generator(prompt))
    
    #Add the assistant response to the chat history
    st.session_state.messages.append({ "role" : "assistant", "content" : response })