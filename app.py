import openai
import streamlit as st

hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []

# Add the prompt
c_prompt = "I want you to act as Purea, the AI chatbot, engaging in a brief and friendly human-like conversation. " \
           "For every conversation, respond naturally and with a medium response , " \
           "as if you were a friendly human friend, while emphasizing the significance of maintaining hygiene and " \
           "cleanliness. Adapt your responses to address the specific question related to hygiene. " \
           "Politely decline to answer any off-topic questions that do not pertain to hygiene and health. don't tell " \
           "Purea / your Qualities "

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input(
        " I'm here to help you get on top of your hygiene routine. Ask me anything related to hygiene"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        for response in openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                temperature=0.00,
                messages=[{"role": m["role"], "content": m["content"] + c_prompt}
                          for m in st.session_state.messages], stream=True):
            full_response += response.choices[0].delta.get("content", "")
            message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown(full_response)
    st.session_state.messages.append({"role": "assistant", "content": full_response})
