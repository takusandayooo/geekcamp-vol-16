import os

import pandas as pd
import requests
from dotenv import load_dotenv
from openai import OpenAI

# load_dotenv()
# print(os.getenv("OPENAI_API_KEY"))

# OpenAIのキーを代入
CLIENT_SECRET = os.getenv("SEARCH_API_KEY")
from news_sum import news_sum
from subject_provide import subject_provider
from subject_sum import subject_sum

talk_data = "就職活動が大変だ"
# 会話データを入力
pro = subject_sum(talk_data)
# 会話の内容を検索プロンプトに変更
news_recent = news_sum(kensaku=pro)
# プロンプトを使って最新のニュース記事を要約して、テキストデータに変換
list = subject_provider(kaiwa=talk_data, news=news_recent)
# ニュース記事と会話内容を踏まえて、楽しそうな話題をリスト化

print(list)
