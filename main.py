from openai import OpenAI
import streamlit as st

st.title("ChatBot proiect TCSV")

#se preia cheia pentru accesarea API-ului de la OpenAI
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"
    #modelul selectat poate sa fie diferit, poate sa fie si gpt-4, sau gpt-4o, dar acestea sunt mai scumpe 

if "messages" not in st.session_state:
    st.session_state.messages = []

#Afisarea istoricului de mesaje
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Ce vrei sa imi zici?"):
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        stream = client.chat.completions.create(
            model=st.session_state["openai_model"],
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        )
        response = st.write_stream(stream)
    st.session_state.messages.append({"role": "assistant", "content": response})