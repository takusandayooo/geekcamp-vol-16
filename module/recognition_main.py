import json
import os

import pandas as pd
import requests
from dotenv import load_dotenv
from openai import OpenAI
from pydantic import BaseModel

from middleware import ApiKeys


def news_sum(api_keys: ApiKeys, kensaku=""):
    # print('news')
    newsAI_key = api_keys.search_api_key
    # NewsAIのキーを代入

    headers = {"X-Api-Key": newsAI_key}
    url = "https://newsapi.org/v2/everything"
    params = {"q": kensaku, "sortBy": "popularity", "pageSize": 20}
    response = requests.get(url, headers=headers, params=params)

    if response.ok:
        data = response.json()
        # print(data)
        df = pd.DataFrame(data["articles"])
        # print('totalResults:', data['totalResults'])
        if data["totalResults"] == 0:
            print("該当する記事がありません")
            return ""
    else:
        return ""
    news_sum_description = df[["description"]]
    news_sumlist = news_sum_description["description"].tolist()

    recent_news = "最新のニュース記事10個:"
    for i in range(len(news_sumlist)):
        # print(i)
        recent_news = (
            recent_news + str(i + 1) + "個めのニュース/n" + str(news_sumlist[i])
        )
    print("最新のニュース；" + recent_news)
    return recent_news


class SubjectProvider(BaseModel):
    subject: list[str]


def subject_provider(api_keys: ApiKeys, kaiwa, news=""):
    data = kaiwa + "," + news
    # dataが会話内容、subjectが話題の配列です。5つの話題を提供します。
    client = OpenAI(api_key=api_keys.openapi_api_key)
    # apikeyを入力
    completion = client.beta.chat.completions.parse(
        model="gpt-4o-mini-2024-07-18",
        messages=[
            {
                "role": "system",
                "content": "あなたは大学生で、飲み会に参加しています。会話の内容、会話のレベルに合わせて、盛り上がりそうな話題を5つ提供します。'最新のニュース記事10個:'と書かれた文字の右からは、最新のニュース記事の要約が10個書かれています。必ず話題の前に:と書いてから出力してください。文中には':'という記号が含まれないようにしてください。例のように出力して下さい 例;:これまでの学生生活で一番面白かったことはなんですか？:旅行で一番印象に残っている場所はどこですか？:ドラマが好きが好きと言っていましたが、最近観た映画やドラマで面白かったのはどんなものですか？:もし無人島に1つだけ持っていけるとしたら何にしますか:どんな恋愛をしてきましたか？",
            },
            {"role": "user", "content": data},
        ],
        response_format=SubjectProvider,
    )

    respond = completion.choices[0].message.content
    json_data = json.loads(respond).get("subject")
    return json_data


def subject_sum(api_keys: ApiKeys, group_data, data):
    # print('話題関数はじめ')
    prompt = f"グループの情報:{group_data},会話内容:{data}"

    # dataが会話内内、会話内容の要約を返します
    client = OpenAI(api_key=api_keys.openapi_api_key)
    # apikeyを入力
    completion = client.chat.completions.create(
        model="gpt-4o-mini-2024-07-18",
        messages=[
            {
                "role": "system",
                "content": "あなたは大学生で、飲み会に参加しています。会話内容を要約して、関係ありそうなニュースを検索するためのプロンプトを表示してください。検索するための空白は,ANDと入力して下さい。例;入力例;おなかすいたね;出力例;食べ物AND話題",
            },
            {"role": "user", "content": prompt},
        ],
    )

    # print('話題の検索プロンプト'+completion.choices[0].message.content)
    return completion.choices[0].message.content


def voice_recognition_func(api_keys: ApiKeys, group_data, talk_data):
    # 会話データを入力
    pro = subject_sum(api_keys, group_data, talk_data)
    # 会話の内容を検索プロンプトに変更
    print(pro)
    news_recent = news_sum(api_keys, kensaku=pro)
    # プロンプトを使って最新のニュース記事を要約して、テキストデータに変換
    list = subject_provider(api_keys, kaiwa=talk_data, news=news_recent)
    # ニュース記事と会話内容を踏まえて、楽しそうな話題をリスト化

    return list


if __name__ == "__main__":
    load_dotenv()
    talk_data = (
        "私は、東京都在住の大学生です。趣味は読書で、最近は小説をよく読んでいます。"
    )
    group_data = "読書好き"
    OPENAI_API_KEY = os.getenv(
        "OPENAI_API_KEY"
    )  # TODO: テストの際には.envファイルにAPIキーを記述
    NEWSAI_KEY = os.getenv("SEARCH_API_KEY")  # NOET: SEARCH_API_KEYはなくても動作します
    api_keys = ApiKeys(openapi_api_key=OPENAI_API_KEY, search_api_key=NEWSAI_KEY)

    voice_recognition_func(api_keys, talk_data)
