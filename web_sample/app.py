from flask import Flask, render_template, request


app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/voice_recognition', methods=['POST'])
def voice_recognition():
    data = request.get_json()
    print(data['result'])
    if data['result'].find("テイクオフ") != -1:
        print('テイクオフ')
    else:
        print('着陸')
    return 'success'

if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0",port="6000")
