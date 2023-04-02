import requests
from bs4 import BeautifulSoup
import csv
import sqlite3
import datetime


class VergeScraper:
    
    def __init__(self, url):
        self.url = url
    
    def get_soup(self):
        response = requests.get(self.url)
        soup = BeautifulSoup(response.content, 'html.parser')
        return soup
    
    def get_articles(self, soup):
        # articles = soup.find_all("ol",class_="relative")
        articles = soup.find_all('div',class_="max-w-content-block-standard md:w-content-block-compact md:max-w-content-block-compact lg:w-[240px] lg:max-w-[240px] lg:pr-10")

        return articles
    
    def extract_info(self, article):
        headline = article.a.text.strip()
        link = "https://theverge.com"+article.find('a')['href']
        author = article.find('a',class_="text-gray-31 hover:shadow-underline-inherit dark:text-franklin mr-8").text
        date = article.find('span',class_="text-gray-63 dark:text-gray-94").text

        return headline, link, author, date
    
    def save_to_csv(self, articles):
        today = datetime.datetime.now().strftime("%d%m%Y")
        filename = f"{today}_verge.csv"
        with open(filename, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['id', 'URL', 'headline', 'author', 'date'])
            for i, article in enumerate(articles):
                headline, link, author, date = self.extract_info(article)
                writer.writerow([i, link, headline, author, date])
                
    def create_database(self):
        conn = sqlite3.connect('verge_articles.db')
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS articles
                    (id INTEGER PRIMARY KEY,
                     url TEXT,
                     headline TEXT,
                     author TEXT,
                     date TEXT)''')
        conn.commit()
        conn.close()
        
    def save_to_database(self, articles):
        conn = sqlite3.connect('verge_articles.db')
        cursor = conn.cursor()
        cursor.execute("SELECT url FROM articles")
        existing_urls = cursor.fetchall()
        existing_urls = [url[0] for url in existing_urls]
        for article in articles:
            headline, link, author, date = self.extract_info(article)
            if link not in existing_urls:
                cursor.execute("INSERT INTO articles (url, headline, author, date) VALUES (?, ?, ?, ?)",
                               (link, headline, author, date))
        conn.commit()
        conn.close()
        
    def run_scraper(self):
        soup = self.get_soup()
        articles = self.get_articles(soup)
        self.save_to_csv(articles)
        self.create_database()
        self.save_to_database(articles)
        print("Scraping complete.")
        

if __name__ == '__main__':
    url = "https://www.theverge.com/"
    scraper = VergeScraper(url)
    scraper.run_scraper()
import requests
from bs4 import BeautifulSoup
import csv
import sqlite3
import datetime


class VergeScraper:
    
    def __init__(self, url):
        self.url = url
    
    def get_soup(self):
        response = requests.get(self.url)
        soup = BeautifulSoup(response.content, 'html.parser')
        return soup
    
    def get_articles(self, soup):
        # articles = soup.find_all("ol",class_="relative")
        articles = soup.find_all('div',class_="max-w-content-block-standard md:w-content-block-compact md:max-w-content-block-compact lg:w-[240px] lg:max-w-[240px] lg:pr-10")

        return articles
    
    def extract_info(self, article):
        headline = article.a.text.strip()
        link = "https://theverge.com"+article.find('a')['href']
        author = article.find('a',class_="text-gray-31 hover:shadow-underline-inherit dark:text-franklin mr-8").text
        date = article.find('span',class_="text-gray-63 dark:text-gray-94").text

        return headline, link, author, date
    
    def save_to_csv(self, articles):
        today = datetime.datetime.now().strftime("%d%m%Y")
        filename = f"{today}_verge.csv"
        with open(filename, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['id', 'URL', 'headline', 'author', 'date'])
            for i, article in enumerate(articles):
                headline, link, author, date = self.extract_info(article)
                writer.writerow([i, link, headline, author, date])
                
    def create_database(self):
        conn = sqlite3.connect('verge_articles.db')
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS articles
                    (id INTEGER PRIMARY KEY,
                     url TEXT,
                     headline TEXT,
                     author TEXT,
                     date TEXT)''')
        conn.commit()
        conn.close()
        
    def save_to_database(self, articles):
        conn = sqlite3.connect('verge_articles.db')
        cursor = conn.cursor()
        cursor.execute("SELECT url FROM articles")
        existing_urls = cursor.fetchall()
        existing_urls = [url[0] for url in existing_urls]
        for article in articles:
            headline, link, author, date = self.extract_info(article)
            if link not in existing_urls:
                cursor.execute("INSERT INTO articles (url, headline, author, date) VALUES (?, ?, ?, ?)",
                               (link, headline, author, date))
        conn.commit()
        conn.close()
        
    def run_scraper(self):
        soup = self.get_soup()
        articles = self.get_articles(soup)
        self.save_to_csv(articles)
        self.create_database()
        self.save_to_database(articles)
        print("Scraping complete.")
        

if __name__ == '__main__':
    url = "https://www.theverge.com/"
    scraper = VergeScraper(url)
    scraper.run_scraper()


# THIS CODE CHECKS THE DATA IN THE TABLE ARTICLES
conn = sqlite3.connect('verge_articles.db')
cursor = conn.cursor()
cursor.execute("SELECT * FROM articles")
rows = cursor.fetchall()
for row in rows:
    print(row)
conn.close()


