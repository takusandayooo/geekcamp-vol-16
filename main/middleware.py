from pydantic import BaseModel


class ApiKeys(BaseModel):
    openapi_api_key: str
    search_api_key: str


def check_api_keys(request) -> dict | None:
    if request.method == "POST":
        body = request.get_json()
        try:
            body["api_keys"]["openai_api_key"]
            body["api_keys"]["search_api_key"]
        except KeyError:
            return {"status_code": 400, "desc": "api keys required"}
