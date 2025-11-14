import streamlit as st
from resources.router import router
from resources.faq import ingest_faq_data, faq_chain
from pathlib import Path
from resources.sql import sql_chain
from resources.small_talk import small_talk_chain

faqs_path = Path(__file__).parent / "resources/faq_data.csv"
ingest_faq_data(faqs_path)

def ask_query(query):
    route = router(query).name
    if route == "faq":
        return faq_chain(query)
    if route == 'sql':
        return sql_chain(query)
    if route == 'small_talk':
        return small_talk_chain(query)
    else:
        return f"{route} is not yet implemented"

st.title("E-Commerce Chatbot")
query = st.chat_input('Write your query')

if "messages" not in st.session_state:
    st.session_state["messages"] = []
for message in st.session_state["messages"]:
    with st.chat_message(message['role']):
        st.markdown(message['content'])
if query:
    with st.chat_message("user"):
        st.markdown(query)
    st.session_state["messages"].append({"role":"user", 'content': query})

    response = ask_query(query)
    with st.chat_message("Assistant"):
        st.markdown(response)
    st.session_state["messages"].append({"role": "Assistant", 'content': response})






