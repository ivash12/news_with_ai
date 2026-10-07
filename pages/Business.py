import streamlit as st
from functions import get_the_news, return_summary, get_sentiment

category = "business"
st.title(f"{category.capitalize()} news summary")

with st.spinner("Generating summary..."):
    texts_list, showed_links, error = get_the_news(category)
    if error:
        st.error(error)
    else:
        summary = return_summary(category, texts_list)
        if summary != "The AI model is busy now. Please, try again later.":
            st.write(summary)
            st.write("References and their sentiment:")
            for index, url in enumerate(showed_links):
                text = texts_list.get(index, "")
                sentiment = get_sentiment(text)
                st.write(f"{sentiment}: {url}")
        else:
            st.write(summary)
