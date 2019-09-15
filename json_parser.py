import json

# articles = { "CNN" : [ [ article_mean, [ [ keyword, salience, mag, score ] ] ] ],
#                      [ next article ], [ next article ] ], "NBC" : , etc. }

def json_to_articles(json_superfile):

    data = ""
    with open(json_superfile, "r") as read_file:
        data = json.load(read_file)

    articles = {}

    # per article
    for article_key in data["article-urls"].keys():

        article_data = data["article-urls"][article_key]
        
        source = article_data["source"]
        
        if source not in articles.keys():
            articles[source] = []

        article_stats = []

        article_overall_sentiment = article_data["sentiment"]
        article_mean = article_overall_sentiment["magnitude"] * \
                       article_overall_sentiment["score"] / \
                       article_overall_sentiment["sentences"]

        article_people = article_data["entity_sentiment"]
        # print(article_people)

        temp_dict = {}
        if type(article_people) == list:
            for i in range(len(article_people)):
                if article_people[i] != None:
                    temp_dict[str(i)] = article_people[i]
            article_people = temp_dict
        # print()
        
        # print(article_people)

        # print()
        article_people_list = []
        for person_key in article_people.keys():
            article_people_list.append([article_people[person_key]["name"], \
                                   article_people[person_key]["salience"], \
                                   article_people[person_key]["sentiment"]["magnitude"], \
                                   article_people[person_key]["sentiment"]["score"]])

        article_stats = [article_mean, article_people_list]

        articles[source].append(article_stats)

    return articles
