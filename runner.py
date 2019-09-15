from json_parser import json_to_articles
from value_calculator import eval_articles_mean, eval_articles_std, eval_articles_pm
import pyrebase
import math
import json
config = {
    "apiKey": "AIzaSyCA64ir3rDXaer9gcExR2k2sMUuUQA_5PU",
    "authDomain": "hack-mit-2e096.firebaseapp.com",
    "databaseURL": "https://hack-mit-2e096.firebaseio.com",
    "storageBucket": "hack-mit-2e096.appspot.com",
    "serviceAccount": "hack-mit-2e096-firebase-adminsdk-u0606-f54e8a8410.json"
}

firebase = pyrebase.initialize_app(config)
db = firebase.database()
data = db.get().val()
with open("sample.json", "w") as fp:
    json.dump(data, fp)
json_superfile = "sample.json"

article_values = json_to_articles(json_superfile)

# mean = eval_articles_mean(article_values)
# std = eval_articles_std(article_values)
pm = eval_articles_pm(article_values)

large_constant = 10000

log_pm = {}
for i in pm.keys():
    
    temp_news_dict = {}
    for j in pm[i].keys():
        
        logPos = 0
        if pm[i][j][0] == 0:
            logPos = 0
        else:
            if pm[i][j][0] * large_constant < 1:
                print("AHHHHHHHHHHHHHH")
            logPos = math.log(pm[i][j][0] * large_constant, 10)

        logNeg = 0
        if pm[i][j][1] == 0:
            logNeg = 0
        else:
            if -pm[i][j][1] * large_constant < 1:
                print("AHHHHHHHHHHHHHH")
            logNeg = -math.log(-pm[i][j][1] * large_constant, 10)
        
        temp_news_dict[j] = [logPos, logNeg]
    log_pm[i] = temp_news_dict

# print(mean)
# print(std)
# print(pm)
print(log_pm)

for n in log_pm:
    for c in log_pm[n]:
        # print(n,c,log_pm[n][c][0],log_pm[n][c][1])
        db.child("news-insights").child(n).push({c: (log_pm[n][c][0], log_pm[n][c][1])})
        db.child("candidates-insights").child(c).push({n: (log_pm[n][c][0], log_pm[n][c][1])})
