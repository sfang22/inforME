import pyrebase
import requests
from bs4 import BeautifulSoup


def get_article_urls(url):
    ret = []
    r = requests.get(url)
    data = r.text
    soup = BeautifulSoup(data, "lxml")

    prev = ""
    for link in soup.find_all('a'):
        article = str(link.get('href'))
        if 'articles/' in article and prev != article:
            prev = article
            print("http://news.google.com" + article[1:])
            ret.append("http://news.google.com" + article[1:])
    return ret

if __name__ == "__main__":
    config = {
        "apiKey": "AIzaSyCA64ir3rDXaer9gcExR2k2sMUuUQA_5PU",
        "authDomain": "hack-mit-2e096.firebaseapp.com",
        "databaseURL": "https://hack-mit-2e096.firebaseio.com",
        "storageBucket": "hack-mit-2e096.appspot.com",
        "serviceAccount": "hack-mit-2e096-firebase-adminsdk-u0606-f54e8a8410.json"
    }

    firebase = pyrebase.initialize_app(config)

    #  Get a reference to the database service
    db = firebase.database()

    past_week = {
        'CNN': 'http://news.google.com/search?q=site%3Acnn.com%20%222020%20election%22%20when%3A7d&hl=en-US&gl=US&ceid=US%3Aen',
        'FOX': 'http://news.google.com/search?q=%20site%3Afoxnews.com%20%222020%20election%22%20when%3A7d&hl=en-US&gl=US&ceid=US%3Aen',
        'BBC': 'http://news.google.com/search?q=site%3Abbc.com%20%222020%20election%22%20when%3A7d&hl=en-US&gl=US&ceid=US%3Aen',
        'WP': 'http://news.google.com/search?q=site%3Awashingtonpost.com%20%222020%20election%22%20when%3A7d&hl=en-US&gl=US&ceid=US%3Aen',
        'ABC': 'http://news.google.com/search?q=site%3Ahttps%3A%2F%2Fabcnews.go.com%2F%20%222020%20election%22%20when%3A7d&hl=en-US&gl=US&ceid=US%3Aen',
        'NBC': 'http://news.google.com/search?q=%20site%3Anbcnews.com%20%222020%20election%22%20when%3A7d&hl=en-US&gl=US&ceid=US%3Aen',
        'CBS': 'http://news.google.com/search?q=%20site%3Awww.cbsnews.com%20%222020%20election%22%20when%3A7d&hl=en-US&gl=US&ceid=US%3Aen',
        'AP': 'http://news.google.com/search?q=%20site%3Awww.apnews.com%20%222020%20election%22%20when%3A7d&hl=en-US&gl=US&ceid=US%3Aen'}

    for source in past_week:
        article_urls = get_article_urls(past_week[source])
        for url in article_urls:
            # data to save
            data = {
                "source": source,
                "url": url
            }
            # Pass the user's idToken to the push method
            db.child("article-urls").push(data)
