from flask import Flask, render_template, request



app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')

@app.route("/follow_up", methods=["GET"])
def follow_up():

    return render_template("follow_up.html")

@app.route('/group_split', methods=['GET'])
def voice_recognition():
    return render_template('group_split.html')


if __name__ == '__main__':
    app.run(debug=True)