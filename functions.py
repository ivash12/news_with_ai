import google
from google import genai
import requests
import trafilatura
from dotenv import load_dotenv
import os
import nltk
import streamlit as st
from nltk.sentiment import SentimentIntensityAnalyzer

nltk.download("vader_lexicon")
load_dotenv()

CACHE_TTL = 20 * 60


class NewsError(Exception):
    pass


@st.cache_data(ttl=CACHE_TTL, show_spinner=False)
def _fetch_news(category):
    currents_api_key = os.getenv("CURRENTS_API_KEY")
    if not currents_api_key:
        raise NewsError("CURRENTS_API_KEY is not set. Add it to your .env file.")
    try:
        response = requests.get(
            "https://api.currentsapi.services/v1/latest-news",
            headers={"Authorization": f"Bearer {currents_api_key}"},
            params={
                "category": category,
                "language": "en",
                "page_size": 10
            },
            timeout=10
        )
    except requests.exceptions.Timeout:
        raise NewsError("The news service took too long to respond. Please, try again later.")
    except requests.exceptions.RequestException:
        raise NewsError("Could not connect to the news service. Please, check your connection and try again.")

    if response.status_code != 200:
        raise NewsError(f"The news service returned an error (HTTP {response.status_code}). Please, try again later.")
    try:
        data = response.json()
    except ValueError:
        raise NewsError("The news service returned an unreadable response. Please, try again later.")
    if not isinstance(data, dict) or "news" not in data:
        raise NewsError("The news service returned an unexpected response. Please, try again later.")

    response = data["news"]
    url_list = []
    showed_links = []
    texts_list = {}
    for i in response:
        url_list.append(i["url"])
    for index, i in enumerate(url_list):
        downloaded = trafilatura.fetch_url(i)
        text = trafilatura.extract(downloaded, output_format="txt")
        if text != None:
            texts_list[index] = (text)
            showed_links.append(i)

    return texts_list, showed_links


def get_the_news(category):
    try:
        texts_list, showed_links = _fetch_news(category)
    except NewsError as e:
        return {}, [], str(e)
    return texts_list, showed_links, None


@st.cache_data(ttl=CACHE_TTL, show_spinner=False)
def _generate_summary(category, texts_list):
    key = os.getenv("GEMINI_API_KEY")
    client = genai.Client(api_key=key)
    response = client.models.generate_content(
        model="gemini-2.5-flash-lite",
        contents=(f"You are a news analyst. Based on the following {category} news articles, "
                  "write a 3-4 sentence overview that identifies the 2-3 dominant themes "
                  "across these articles. Do not mention each article individually. "
                  "Synthesize the key themes into one coherent paragraph, "
                  "do not list articles one by one. Do not start with 'Currently' or 'Recently'. "
                  "Ignore any garbled or unreadable text. "
                  f"Articles: {texts_list}"))
    return response.text


def return_summary(category, texts_list):
    try:
        return _generate_summary(category, texts_list)
    except google.genai.errors.ServerError:
        return "The AI model is busy now. Please, try again later."

def get_sentiment(text):
    sia = SentimentIntensityAnalyzer()
    score = sia.polarity_scores(text)["compound"]
    if score >= 0.05:
        return "Positive"
    elif score <= -0.05:
        return "Negative"
    else:
        return "Neutral"



