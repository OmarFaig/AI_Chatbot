import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
from urllib.parse import urljoin

def scrape_article_links(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    response = requests.get(url, headers=headers, timeout=10)
    response.raise_for_status()
    soup = BeautifulSoup(response.content, 'html.parser')
    links = []
    for link in soup.find_all('a', href=True):
        href = link['href']
        if 'article' in href:
            full_url = urljoin(url, href)
            links.append(full_url)
    print(f"Found {len(links)} article links.")
    return links

def scrape_article(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    response = requests.get(url, headers=headers, timeout=10)
    response.raise_for_status()
    soup = BeautifulSoup(response.content, 'html.parser')
    title = soup.find('h1').get_text() if soup.find('h1') else 'No Title'
    paragraphs = soup.find_all('p')
    content = ' '.join([p.get_text() for p in paragraphs])
    return {'title': title, 'content': content}

def save_to_csv(data, filename):
    df = pd.DataFrame(data)
    df.to_csv(filename, index=False)

if __name__ == "__main__":
    base_url = 'https://en.wikipedia.org/wiki/S%26P_500#Derivatives'
    article_links = scrape_article_links(base_url)

    articles = []
    for link in article_links:
        try:
            article = scrape_article(link)
            print(f"Scraped: {article['title']}")
            articles.append(article)
        except requests.exceptions.RequestException as e:
            print(f"Failed to scrape {link}: {e}")
        except Exception as e:
            print(f"An error occurred while scraping {link}: {e}")
        time.sleep(1)  # Be polite and avoid overwhelming the server

    save_to_csv(articles, 'financial_news.csv')
    print("Data scraped and saved to financial_news.csv")