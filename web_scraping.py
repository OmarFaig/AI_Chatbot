import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

def scrape_article_links(url):
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.content, 'html.parser')
    links = []
    for link in soup.find_all('a', href=True):
        if 'article' in link['href']:
            links.append(link['href'])
    return links

def scrape_article(url):
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.content, 'html.parser')
    title = soup.find('h1').get_text()
    paragraphs = soup.find_all('p')
    content = ' '.join([p.get_text() for p in paragraphs])
    return {'title': title, 'content': content}

def save_to_csv(data, filename):
    df = pd.DataFrame(data)
    df.to_csv(filename, index=False)

if __name__ == "__main__":
    base_url = 'https://finance.yahoo.com/news/union-workers-picket-3rd-day-212337268.html'
    article_links = scrape_article_links(base_url)

    articles = []
    for link in article_links:
        article_url = base_url + link
        article = scrape_article(article_url)
        print(f"Scraped: {article['title']}")
        articles.append(article)
        time.sleep(1)  # Be polite and avoid overwhelming the server

    save_to_csv(articles, 'financial_news.csv')
    print("Data scraped and saved to financial_news.csv")