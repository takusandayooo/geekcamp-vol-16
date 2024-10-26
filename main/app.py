from dotenv import load_dotenv
from flask import Flask, abort, jsonify, render_template, request
from pydantic import ValidationError

from module.group_split import Groups, Introductions, split_groups
from module.follow_up import AI_follow_up_questions


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
    if request.method == "POScT":
        data = request.get_json()
        print(data)
        AI_follow_up_questions(data["result"])
        return jsonify({"status": "success", "result": data})

    else:
        return render_template("table.html")


@app.route("/group_split", methods=["GET", "POST"])
def group_split():
    if request.method == "GET":
        return render_template("group_split.html")
    else:
        try:
            data = request.get_json()
            intros = Introductions(**data["intros"])
        except ValidationError:
            abort(
                500,
                description="原因不明のエラーが発生しました。時間を空けて実行して下さい。",
            )

        groups: Groups | None = split_groups(intros)
        if groups is None:
            abort(
                500,
                description="原因不明のエラーが発生しました。時間を空けて実行して下さい。",
            )
        return jsonify(groups.model_dump())


if __name__ == "__main__":
    app.run(debug=True)
