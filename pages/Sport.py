import streamlit as st
from functions import get_the_news, return_summary

category = "sports"
st.title(f"{category.capitalize()} news summary")

with st.spinner("Generating summary..."):
    texts_list, showed_links = get_the_news(category)
    summary = return_summary(category, texts_list)
    if summary != "The AI model is busy now. Please, try again later.":
        st.write(summary)
        st.write("References:")
        for i in showed_links:
            st.markdown(i)
    else:
        st.write(summary)