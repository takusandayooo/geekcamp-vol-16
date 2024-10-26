import requests
import pandas as pd
from dotenv import load_dotenv


import os


def news_sum(kensaku=""):
    # print('news')
    newsAI_key = os.getenv("SEARCH_API_KEY")
    # NewsAIのキーを代入

    headers = {"X-Api-Key": newsAI_key}
    url = "https://newsapi.org/v2/everything"
    params = {"q": kensaku, "sortBy": "popularity", "pageSize": 20}
    response = requests.get(url, headers=headers, params=params)

    if response.ok:
        data = response.json()
        df = pd.DataFrame(data["articles"])
        # print('totalResults:', data['totalResults'])
    news_sum = df[["description"]]
    news_sumlist = news_sum["description"].tolist()

    recent_news = "最新のニュース記事10個:"
    for i in range(len(news_sumlist)):
        # print(i)
        recent_news = (
            recent_news + str(i + 1) + "個めのニュース/n" + str(news_sumlist[i])
        )
    print("最新のニュース；" + recent_news)
    return recent_news
