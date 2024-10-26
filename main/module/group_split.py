from openai import OpenAI
from pydantic import BaseModel


class Group(BaseModel):
    group_name: str
    overview: str
    usernames: list[str]


class _GroupList(BaseModel):
    groups: list[Group]


class Introduction(BaseModel):
    username: str
    content: str


class _IntroductionList(BaseModel):
    introductions: list[Introduction]


def split_groups_by(intros: list[Introduction]) -> list[Group] | None:
    if len(intros) == 0:
        return None

    intro_json: str = _IntroductionList(introductions=intros).model_dump_json()

    client = OpenAI()
    response = client.beta.chat.completions.parse(
        model="gpt-4o-mini-2024-07-18",
        response_format=_GroupList,
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
                "content": intro_json,
            },
        ],
    )

    group_list: _GroupList | None = response.choices[0].message.parsed
    if group_list is None:
        return None
    return group_list.groups
