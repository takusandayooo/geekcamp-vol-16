from dotenv import load_dotenv
from openai import OpenAI
from pydantic import BaseModel

load_dotenv()


class Group(BaseModel):
    group_name: str
    feature: str
    name: list[str]


class Groups(BaseModel):
    groups: list[Group]


class Introduction(BaseModel):
    name: str
    self_introduction: str


class Introductions(BaseModel):
    self_introductions: list[Introduction]

    def add_introduction(self, name: str, intro: str):
        introduction = Introduction(name=name, self_introduction=intro)
        self.self_introductions.append(introduction)


def split_groups(intros: Introductions) -> Groups | None:
    client = OpenAI()
    intros_json = intros.model_dump_json()
    response = client.beta.chat.completions.parse(
        model="gpt-4o-mini-2024-07-18",
        response_format=Groups,
        messages=[
            {
                "role": "system",
                "content": """
# やること

自己紹介文を元に、似ている人をグループ分けしてください。同じ趣味や関心を持っている人、共通の経験を持つ人を一緒にしてください。
    """,
            },
            {
                "role": "user",
                "content": intros_json,
            },
        ],
    )

    return response.choices[0].message.parsed
