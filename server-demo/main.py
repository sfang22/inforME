import os
from flask import Flask,render_template

#Initialize Flask
app = Flask(__name__)

#Initialize Firebase DB
import pyrebase

config = {
  "apiKey": "AIzaSyCA64ir3rDXaer9gcExR2k2sMUuUQA_5PU",
  "authDomain": "hack-mit-2e096.firebaseapp.com",
  "databaseURL": "https://hack-mit-2e096.firebaseio.com",
  "storageBucket": "hack-mit-2e096.appspot.com",
  "serviceAccount": "hack-mit-2e096-firebase-adminsdk-u0606-f54e8a8410.json"
}
firebase = pyrebase.initialize_app(config)

@app.route('/')
def demo():
    return render_template('bars.html')


@app.route('/news/All', methods=['GET'])
def api_overall():
    db = firebase.database()
    insights = db.child("candidates-insights").get().val()
    result = {}
    f = lambda lst: sum(lst) / len(lst)
    for candidate in insights:
        print(candidate)
        val_1 = []
        val_2 = []
        for _, val in insights[candidate].items():
            [value_1, value_2] = list(val.values())[0]
            val_1.append(value_1)
            val_2.append(value_2)
        result[candidate] = [f(val_1), f(val_2)]
    return result

@app.route('/news/<news_name>', methods=['GET'])
def api_news(news_name):
    news_name = news_name.replace('_', ' ')
    db = firebase.database()
    insights = db.child("news-insights").child(news_name).get().val()
    result = {}
    for key in insights:
        result.update(insights[key])
    return result

@app.route('/candidates/<candidate_name>', methods=['GET'])
def api_candidates(candidate_name):
    candidate_name = candidate_name.replace('_', ' ')
    db = firebase.database()
    insights = db.child("candidates-insights").child(candidate_name).get().val()
    result = {}
    for key in insights:
        result.update(insights[key])
    return result

if __name__ == "__main__":
    app.run(host= '0.0.0.0')
