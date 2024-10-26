from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()

import os
OPEN_AI_API_KEY = os.getenv('OPEN_AI_API_KEY')


#NOTE:自己紹介してもらった内容から、追加の質問があった場合に返答する関数
def AI_follow_up_questions(chat):
    client = OpenAI(api_key=OPEN_AI_API_KEY)
    system_prompt="""
        あなたは、ユーザーの自己紹介をもとに追加質問を生成するアシスタントです。ユーザーの自己紹介が不十分な場合、関連する情報を補完するための一般的な質問を以下の形式で提示してください。質問が不要な場合は「false」を返してください。

        質問は以下の基準を満たす必要があります：
        - 自己紹介の明確化に役立つものであること
        - できるだけ簡潔で具体的であること
        - 一般的な内容で、自己紹介に対する具体的な深掘りをしないこと

        質問の形式は以下の番号付きフォーマットに従ってください：

        1. どの大学に通っていますか？
        2. 専攻は何ですか？
        3. 好きな作家や小説のジャンルはありますか？
        4. 読書以外に趣味はありますか？
        5. 休日はどのように過ごしていますか？
    """
    prompt=f"""
        以下の自己紹介をもとに、追加の質問が必要かどうかを判断してください。必要な場合は、以下のフォーマットに従って一般的な質問を番号付きで提示してください。質問が不要な場合は「false」を返してください。

        自己紹介: [{chat}]
        """
    completion = client.chat.completions.create(
    model="gpt-4o-mini-2024-07-18",
    messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": prompt}
    ]
    )
    print(completion.choices[0].message)
    response_content=completion.choices[0].message.content
    if response_content=="false":
        return response_content
    else:
        return_text= response_content.split("\n")
        print(return_text)

if __name__ == "__main__":
    chat = "私は、東京都在住の大学生です。趣味は読書で、最近は小説をよく読んでいます。"
    print(AI_follow_up_questions(chat))
