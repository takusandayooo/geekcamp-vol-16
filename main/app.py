from dotenv import load_dotenv
from flask import Flask, abort, jsonify, render_template, request
from pydantic import ValidationError

from .middleware import ApiKeys, check_api_keys
from .module.follow_up import AI_follow_up_questions
from .module.group_split import (
    Group,
    Introduction,
    split_groups_by,
)
from .module.recognition_main import voice_recognition_func

load_dotenv()


app = Flask(__name__)


@app.before_request
def require_api_keys():
    err = check_api_keys(request)
    if err:
        return jsonify({"error": err["desc"]}), err["status_code"]


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/follow_up", methods=["GET", "POST"])
def follow_up():
    if request.method == "POST":
        data = request.get_json()
        print(data)
        api_keys = ApiKeys(**data["api_keys"])
        result = AI_follow_up_questions(api_keys, data["result"])
        print(result)
        return jsonify({"status": "success", "result": result})
    else:
        return render_template("follow_up.html")


@app.route("/table", methods=["GET", "POST"])
def table():
    if request.method == "GET":
        return render_template("table.html")
    else:
        body = request.get_json()
        api_keys = ApiKeys(**body["api_keys"])
        try:
            intros = [Introduction(**intro) for intro in body["data"]]
        except ValidationError:
            abort(
                500, "サーバー内で問題が生じました。時間を空けてから実行してください。"
            )

        groups: list[Group] | None = split_groups_by(api_keys, intros)
        if groups is None:
            return jsonify({"result": []})

        result = [group.model_dump() for group in groups]
        return jsonify({"result": result})


@app.route("/voice_recognition", methods=["POST", "GET"])
def voice_recognition():
    if request.method == "GET":
        return render_template("voice_recognition.html")
    else:
        data = request.get_json()
        api_keys = ApiKeys(**data["api_keys"])
        print(data["result"])
        result = voice_recognition_func(api_keys, data["result"])
        return jsonify({"status": "success", "result": result})


if __name__ == "__main__":
    app.run(debug=True)
