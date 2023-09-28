import requests, json
from bs4 import BeautifulSoup
from transformers import pipeline

from time import sleep, perf_counter
from selenium import webdriver
# from twocaptcha import TwoCaptcha
from os import environ as env_variable
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

# List of news websites
websites = [
    {
        'name': 'Punch',
        'url': 'https://punchng.com/',
        'article_class': 'post-content'
    },
    # {
    #     'name': 'Vanguard',
    #     'url': 'https://www.vanguardngr.com/',
    #     'article_class': 'entry-item'
    # },
    # {
    #     'name': 'Premium Times',
    #     'url': 'https://www.premiumtimesng.com/',
    #     'article_class': 'post-item'
    # },
    # {
    #     'name': 'The Guardian Nigeria',
    #     'url': 'https://guardian.ng/',
    #     'article_class': 'item'
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
    print(f"Scraping articles from {website['name']}\n")
    baseurl = website['url']
    article_class = website['article_class']
    response = requests.get(baseurl)
    soup = BeautifulSoup(response.content, 'html.parser')
    articles = soup.find_all(class_=article_class)

    news_info = {}
    for idx, article in enumerate(articles, 1):
        # if idx != 5: continue  # DEBUGGING(REMOVE WHEN DONE)
        title = article.find('a').text.strip()
        posturl = article.find('a')['href']
        newspage_response = requests.get(posturl)
        news_soup = BeautifulSoup(newspage_response.content, 'html.parser')
        news_paragraphs = news_soup.find('div', class_="post-content").find_all('p')
        news = news_paragraphs[0].text
        newslist = []
        if len(news_paragraphs[0].text) > 200: # 200 Characters
            continue
        if len(news_paragraphs[0].text) < 200: # 200 Characters
        # if len(news) < 200: # 200 Characters
            for news_paragraph in news_paragraphs:
                # next_element = news_paragraph.next_element
                if news_paragraph.text not in newslist:
                    newslist.append(news_paragraph.text)
                    # if "deployed this money?,’’ he queried" in news_paragraph.text:
                    #     print(news_paragraph.text)
                    # print(news_paragraph.text)
            news = " ".join(newslist)
            # news = " ".join(news_paragraphs)
            print("#"*50)
            news_info[title] = news
        if idx == 20: break

    return news_info  # Scraped Articles

for site_no, website in zip(range(len(websites)), websites):
    newsinfo: dict = scrape(websites[site_no])
    # with open(f"{website['name']}_news_info.json", "a") as file:
    #     json.dump(newsinfo, file)


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
