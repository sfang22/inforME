import requests
from bs4 import BeautifulSoup

def get_content(tag):
    if isinstance(tag, str):
        return tag
    elif isinstance(tag, list):
        paragraph = []
        for item in tag:
            paragraph.append(get_content(item))
        return " ".join(paragraph)
    else:
        return get_content(tag.contents)


def scrape_url_cnn(url):
    ret = []
    r = requests.get(url)
    data = r.text
    soup = BeautifulSoup(data, "lxml")
    for paragraph in soup.find_all("div", {"class": "zn-body__paragraph"}):
        paragraph = get_content(paragraph)
        ret.append(paragraph)
    return " ".join(ret)


def scrape_url_fox(url):
    ret = []
    r = requests.get(url)
    data = r.text
    soup = BeautifulSoup(data, "lxml")
    for paragraph in soup.find_all("p"):
        string_p = str(paragraph)
        if "copyright" in string_p or "<strong>" in string_p:
            continue
        paragraph = get_content(paragraph)
        ret.append(paragraph)

    return " ".join(ret)

def scrape_url_bbc(url):
    ret = []
    r = requests.get(url)
    data = r.text
    soup = BeautifulSoup(data, "lxml")
    for paragraph in soup.find_all("p"):
        string_p = str(paragraph)
        if "__" in string_p:
            continue
        paragraph = get_content(paragraph)
        ret.append(paragraph)

    return " ".join(ret)

def scrape_url_vanilla(url):
    ret = []
    r = requests.get(url)
    data = r.text
    soup = BeautifulSoup(data, "lxml")
    for paragraph in soup.find_all("p"):
        paragraph = get_content(paragraph)
        ret.append(paragraph)

    return " ".join(ret)

def scrape_url(source, url):
    source_to_function = {"CNN" : scrape_url_cnn,
                          "FOX" : scrape_url_fox,
                          "BBC" : scrape_url_bbc,
                          "CBS" : scrape_url_bbc
                          }
    if source in source_to_function:
        return source_to_function[source](url)
    else:
        return scrape_url_vanilla(url)

if __name__ == "__main__":
    pass
    # print(scrape_url("CNN", "http://www.cnn.com/2019/07/02/politics/elizabeth-warren-kamala-harris-election-2020/index.html"))
    # print(scrape_url("FOX", "http://www.foxnews.com/media/andrew-yang-teases-houston-debate"))
    # print(scrape_url("BBC", "http://www.bbc.com/news/world-us-canada-49601678"))
    # print(scrape_url("WP", "http://beta.washingtonpost.com/politics/president-trump-trails-potential-democratic-challengers-in-2020-test/2019/09/10/82980d72-d36a-11e9-9610-fb56c5522e1c_story.html"))
    # print(scrape_url("ABC", "http://abcnews.go.com/Politics/ahead-debate-beto-orourke-returns-texas-doubling-gun/story?id=65558396"))
    # print(scrape_url("CBS", "http://www.cbsnews.com/news/where-the-2020-candidates-stand-on-climate-change-town-hall-2019-09-03/"))
    # print(scrape_url("NBC", "https://www.nbcnews.com/politics/2020-election/texas-gop-lawmakers-tells-beto-o-rourke-my-ar-ready-n1053986"))
    # print(scrape_url("AP", "https://www.apnews.com/3801ceee28554b0988641635b538c6c0"))