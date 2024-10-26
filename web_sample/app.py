from flask import Flask, render_template, request


app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/voice_recognition', methods=['POST'])
def voice_recognition():
    data = request.get_json()
    print(data['result'])

if __name__ == '__main__':
    app.run(debug=True)
