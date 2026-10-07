import google
from google import genai
import requests
import trafilatura
from dotenv import load_dotenv
import os
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer

nltk.download("vader_lexicon")
load_dotenv()

#returns the news, articles' links and an error message (None if everything went fine) from CURRENTS_API
def get_the_news(category):
    currents_api_key = os.getenv("CURRENTS_API_KEY")
    if not currents_api_key:
        return {}, [], "CURRENTS_API_KEY is not set. Add it to your .env file."
    try:
        response = requests.get(
            "https://api.currentsapi.services/v1/latest-news",
            params={
                "apiKey": currents_api_key,
                "category": category,
                "language": "en",
                "page_size": 10
            },
            timeout=10
        )
    except requests.exceptions.Timeout:
        return {}, [], "The news service took too long to respond. Please, try again later."
    except requests.exceptions.RequestException:
        # the exception text contains the request URL with the API key, so it is not shown
        return {}, [], "Could not connect to the news service. Please, check your connection and try again."

    if response.status_code != 200:
        return {}, [], f"The news service returned an error (HTTP {response.status_code}). Please, try again later."
    try:
        data = response.json()
    except ValueError:
        return {}, [], "The news service returned an unreadable response. Please, try again later."
    if not isinstance(data, dict) or "news" not in data:
        return {}, [], "The news service returned an unexpected response. Please, try again later."

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

    return texts_list, showed_links, None

#returns summary of the articles
def return_summary(category, texts_list):
    key = os.getenv("GEMINI_API_KEY")
    client = genai.Client(api_key=key)
    try:
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
    except google.genai.errors.ServerError:
        return "The AI model is busy now. Please, try again later."

# sentiment analysis
def get_sentiment(text):
    sia = SentimentIntensityAnalyzer()
    score = sia.polarity_scores(text)["compound"]
    if score >= 0.05:
        return "Positive"
    elif score <= -0.05:
        return "Negative"
    else:
        return "Neutral"



