from requests import get
from bs4 import BeautifulSoup
import os
import pandas as pd

def scrape_codeup():
    url = 'https://codeup.com/blog/'
    headers = {'User-Agent': 'Codeup Data Science'} 
    response = get(url, headers=headers)

    # Make a soup variable holding the response content
    soup = BeautifulSoup(response.content, 'html.parser')

    urls = [urls['href'] for urls in soup.select('h2 a[href]')]

    articles = []

    for url in urls:
        
        url_response = get(url, headers=headers)
        soup = BeautifulSoup(url_response.text)
        
        title = soup.find('h1', class_='entry-title').text
        content = soup.find('div', class_='entry-content').text.strip()
        dates = [date.text for date in soup.find_all('span', class_='published')]

        article_dict = {
            'title': title,
            'content': content,
            'date': dates
        }
        
        articles.append(article_dict)

    df = pd.DataFrame(articles)

    df.to_csv('codeup_blogs.csv')

    return df
