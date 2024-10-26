from dotenv import load_dotenv
from flask import Flask, abort, jsonify, render_template, request
from module.follow_up import AI_follow_up_questions
from module.group_split import (
    Group,
    Introduction,
    split_groups_by,
)
from module.recognition_main import voice_recognition_func
from pydantic import ValidationError

load_dotenv()

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/follow_up", methods=["GET", "POST"])
def follow_up():
    if request.method == "POST":
        data = request.get_json()
        print(data)
        result = AI_follow_up_questions(data["result"])
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
        try:
            intros = [Introduction(**intro) for intro in body["data"]]
        except ValidationError:
            abort(
                500, "サーバー内で問題が生じました。時間を空けてから実行してください。"
            )

        groups: list[Group] | None = split_groups_by(intros)
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
        print(data["result"])
        result = voice_recognition_func(data["result"])
        return jsonify({"status": "success", "result": result})


if __name__ == "__main__":
    app.run(debug=True)
