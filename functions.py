from google import genai
import requests
import trafilatura
from dotenv import load_dotenv
import os

#returns the news and articles' links from CURRENTS_API
def get_the_news(category):
    load_dotenv()
    currents_api_key = os.getenv("CURRENTS_API_KEY")
    response = requests.get(
        "https://api.currentsapi.services/v1/latest-news",
        params={
            "apiKey": currents_api_key,
            "category": category,
            "language": "en",
            "page_size": 10
        }
    )
    response = response.json()["news"]
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

#returns summary of the articles
def return_summary(category, texts_list):
    client = genai.Client()
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

