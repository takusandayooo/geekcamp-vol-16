from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

import os

# CLIENT_SECRET = os.getenv("CLIENT_SECRET")


def subject_provider(kaiwa, news=""):
    data = kaiwa + "," + news
    # dataが会話内容、subjectが話題の配列です。5つの話題を提供します。
    client = OpenAI()
    # apikeyを入力
    completion = client.chat.completions.create(
        model="gpt-4o-mini-2024-07-18",
        messages=[
            {
                "role": "system",
                "content": "あなたは大学生で、飲み会に参加しています。会話の内容、会話のレベルに合わせて、盛り上がりそうな話題を5つ提供します。'最新のニュース記事10個:'と書かれた文字の右からは、最新のニュース記事の要約が10個書かれています。必ず話題の前に:と書いてから出力してください。文中には':'という記号が含まれないようにしてください。例のように出力して下さい 例;:これまでの学生生活で一番面白かったことはなんですか？:旅行で一番印象に残っている場所はどこですか？:ドラマが好きが好きと言っていましたが、最近観た映画やドラマで面白かったのはどんなものですか？:もし無人島に1つだけ持っていけるとしたら何にしますか:どんな恋愛をしてきましたか？",
            },
            {"role": "user", "content": data},
        ],
    )

    respond = completion.choices[0].message.content
    # 出力された内容をrespondに代入

    subject = respond.split(":")
    subject.remove("")
    return subject
