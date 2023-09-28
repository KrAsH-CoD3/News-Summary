import requests, json
from bs4 import BeautifulSoup
# from transformers import pipeline

# from time import sleep, perf_counter
# from selenium import webdriver
# from twocaptcha import TwoCaptcha
# from os import environ as env_variable
# from selenium.webdriver.common.by import By
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.common.exceptions import TimeoutException, NoSuchElementException

# List of news websites
websites = [
    # {
    #     'name': 'Punch',
    #     'url': 'https://punchng.com/',
    #     'hp_tag': 'p',
    #     'hp_article_class': 'post-content',
    #     'pp_tag': 'p',
    #     'pp_outter_element': 'div',
    #     'pp_article_class': 'post-content',
    # },
    # {
    #     'name': 'Premium Times',
    #     'url': 'https://premiumtimesng.com/',
    #     'hp_tag': 'h2',
    #     'hp_article_class': 'jeg_post_title',
    #     'pp_tag': 'p',
    #     'pp_outter_element': 'div',
    #     'pp_article_class': 'content-inner',
    # },
    {
        'name': 'The Guardian Nigeria',
        'url': 'https://guardian.ng/',
        'hp_tag': 'div',
        'hp_article_class': 'headline',
        'pp_tag': 'p',
        'pp_outter_element': 'div',
        'pp_article_class': 'content',
    },
    # {
    #     'name': 'Vanguard',
    #     'url': 'https://vanguardngr.com/',
    #     'tag': 'p'
    #     'article_class': 'entry-title'
    # },
    # {
    #     'name': 'Daily Trust',
    #     'url': 'https://dailytrust.com/',
    #     'article_class': 'story-box'
    # }
]


# Function to fetch full article content
def get_full_article(article_url):
    response = requests.get(article_url)
    soup = BeautifulSoup(response.content, 'html.parser')
    article_body = soup.find(class_='post-content')
    paragraphs = article_body.find_all('p')
    full_article = ' '.join([p.text for p in paragraphs])
    return full_article


# Function to scrape and summarize articles
def scrape(website) -> dict:
    print(f"Getting {website['name']} News...\n")
    baseurl = website['url']
    article_class = website['hp_article_class']
    response = requests.get(baseurl)
    soup = BeautifulSoup(response.content, 'html.parser')
    articles = soup.find_all(class_=article_class)

    news_info = {}
    for idx, article in enumerate(articles, 1):
        title = article.find('a').text.strip()
        posturl = article.find('a')['href']
        newspage_response = requests.get(posturl)
        news_soup = BeautifulSoup(newspage_response.content, 'html.parser')
        news_paragraphs = news_soup.find(website['pp_outter_element'], \
            class_=website['pp_article_class']).find_all(website['pp_tag'])
        news = news_paragraphs[0].text
        if len(news) > 250: # 250 Characters
            news_info[title] = news.strip()
        else:
            newslist = []
            for news_paragraph in news_paragraphs:
                if news_paragraph.text not in newslist:
                    newslist.append(news_paragraph.text)
            news = " ".join(newslist).strip()
            news_info[title] = news
            newslist.clear()
            # print("#"*50)
        if idx == 13: break

    return news_info  # Scraped Articles

for site_no, website in zip(range(len(websites)), websites):
    newsinfo: dict = scrape(websites[site_no])
    with open(f"{website['name']}_news.json", "a") as file:
        json.dump(newsinfo, file)


# import requests
# import nltk
# import pandas as pd

# def get_news_summary(url):
#   response = requests.get(url)
#   text = response.text
#   summary = nltk.sent_tokenize(text)[:3]
#   sentiment = nltk.sentiment.vader.SentimentIntensityAnalyzer().polarity_scores(text)
#   return {
#     "title": response.headers["title"],
#     "author": response.headers["author"],
#     "summary": summary,
#     "sentiment": sentiment
#   }

# def export_to_csv(data):
#   df = pd.DataFrame(data)
#   df.to_csv("news_summary.csv")

# if __name__ == "__main__":
#   url = "https://www.bbc.com/news/world-us-canada-61945504"
#   data = get_news_summary(url)
#   export_to_csv(data)
