import streamlit as st

st.title("News with AI")
st.write("Choose the topic you would like to see the news summary.")
topics = ["Science", "Finance", "Business", "Technology", "Health", "Sport",  "Politics", "Education"]

for topic in topics:
    if st.button(topic):
        st.session_state["topic"] = topic
        st.switch_page(f"pages/{topic}.py")