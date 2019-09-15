from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types

import pyrebase
import article_scraper
import json
config = {
  "apiKey": "AIzaSyCA64ir3rDXaer9gcExR2k2sMUuUQA_5PU",
  "authDomain": "hack-mit-2e096.firebaseapp.com",
  "databaseURL": "https://hack-mit-2e096.firebaseio.com",
  "storageBucket": "hack-mit-2e096.appspot.com",
  "serviceAccount": "hack-mit-2e096-firebase-adminsdk-u0606-f54e8a8410.json"
}

NAME_MAPPING = {"Trump": "Donald Trump", "Donald J Trump": "Donald Trump", "Castro":  "Julian Castro",
             "Booker": "Cory Booker", "Yang": "Andrew Yang", "Warren": "Elizabeth Warren", "Biden": "Joe Biden",
             "Sanders": "Bernie Sanders",  "Harris": "Kamala Harris",  "O'Rourke": "Beto O'Rourke",
             "Buttigieg": "Pete Buttigieg", "Klobuchar": "Amy Klobuchar", "Steyer": "Tom Steyer"}
CANDIDATES = {"Trump", "Donald Trump", "Donald J Trump", "Castro", "Julian Castro", "Booker", "Cory Booker", "Yang", "Andrew Yang", "Warren", "Elizabeth Warren", "Biden", "Joe Biden", "Sanders", "Bernie Sanders", "Harris", "Kamala Harris", "O'Rourke", "Beto O'Rourke", "Buttigieg", "Pete Buttigieg", "Klobuchar", "Amy Klobuchar", "Steyer", "Tom Steyer"}
firebase = pyrebase.initialize_app(config)


def process_sentiment(annotations):
    score = annotations.document_sentiment.score
    magnitude = annotations.document_sentiment.magnitude
    sentences = len(annotations.sentences)
    return {"score": score, "magnitude": magnitude, "sentences": sentences}

def process_entity_sentiment(annotations):
    all_sentiments = {}

    for x in enumerate(annotations.entities):
        if x[1].name in CANDIDATES:
            name = x[1].name if x[1].name not in NAME_MAPPING else NAME_MAPPING[x[1].name]
            all_sentiments[x[0]] = {"name": name, "salience": x[1].salience, "sentiment": {"score": x[1].sentiment.score, "magnitude": x[1].sentiment.magnitude}}

    return all_sentiments

def analyze(movie_review_filename):
  """Run a sentiment analysis request on text within a passed filename."""
  client = language.LanguageServiceClient()

  with open(movie_review_filename, 'r') as review_file:
    # Instantiates a plain text document.
    content = review_file.read()

  document = types.Document(
    content=content,
    type=enums.Document.Type.PLAIN_TEXT)

  annotations_sentiment = client.analyze_sentiment(document=document, timeout=10000)
  annotations_entity_sentiment = client.analyze_entity_sentiment(document=document, timeout=10000)

  return process_sentiment(annotations_sentiment), process_entity_sentiment(annotations_entity_sentiment)


def real_urls():
    db = firebase.database()
    urls = db.child("article-urls").get()
    for url_id in urls.val():
        url_info = urls.val()[url_id]
        action = "None"
        if ("sentiment" not in url_info) and ("entity_sentiment" not in url_info):
            action = "Build"
            #save article content to txt file
            article_content = article_scraper.scrape_url(url_info["source"],url_info["url"])
            with open("sample_news.txt", "w") as text_file:
                text_file.write(article_content)

            #google api sentiment analysis
            sentiment, entity_sentiment = analyze("sample_news.txt")

            db.child("article-urls").child(url_id).update({"sentiment": sentiment})
            db.child("article-urls").child(url_id).update({"entity_sentiment": entity_sentiment})
        elif "entity_sentiment" not in url_info:
            db.child("article-urls").child(url_id).remove()
            action = "remove"
        print(url_id, action)

if __name__ == "__main__":
    real_urls()
    # print(analyze("sample_news.txt"))