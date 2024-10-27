from pydantic import BaseModel, Field


class ApiKeys(BaseModel):
    openapi_api_key: str
    search_api_key: str = Field(default="")


def check_api_keys(request) -> dict | None:
    if request.method == "POST":
        body = request.get_json()

        try:
            body["api_keys"]
            body["api_keys"]["openai_api_key"]
        except KeyError:
            return {"status_code": 400, "desc": "openai_api_key keys required"}
