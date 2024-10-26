from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

import os

openAI_key = os.getenv("OPEN_AI_API_KEY")
# OpenAIのキーを代入
CLIENT_SECRET = os.getenv("CLIENT_SECRET")


def subject_sum(data):
    # print('話題関数はじめ')

    # dataが会話内内、会話内容の要約を返します
    client = OpenAI()
    # apikeyを入力
    completion = client.chat.completions.create(
        model="gpt-4o-mini-2024-07-18",
        messages=[
            {
                "role": "system",
                "content": "あなたは大学生で、飲み会に参加しています。会話内容を要約して、関係ありそうなニュースを検索するためのプロンプトを表示してください。検索するための空白は,ANDと入力して下さい。例;入力例;おなかすいたね;出力例;食べ物AND話題",
            },
            {"role": "user", "content": data},
        ],
    )

    # print('話題の検索プロンプト'+completion.choices[0].message.content)
    return completion.choices[0].message.content
