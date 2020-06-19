import requests
from bs4 import BeautifulSoup
import sys
import json

def getWebsite(url):
  r = requests.get(url)
  soup = BeautifulSoup(r.content, features = "html.parser")
  return soup

titles = []
articles = []

input = sys.argv[1]
inputx = [x.lower() for x in input.split(" ")]

if inputx[0] == "get":
  if inputx[1] == "news" or inputx[1] == "articles" or inputx[1] == "reviews":
    if inputx[3] is not None:
      lst = inputx[3:]
      topic = " ".join(lst)
elif inputx[0] == "news" or inputx[0] == "articles" or inputx[0] == "reviews":
  if inputx[2] is not None:
    lst = inputx[2:]
    topic = " ".join(lst)
else:
  topic = None

#topic = "Samsung Galaxy S20"

if topic is not None:
  urls = ["https://www.cnet.com/reviews/"]

  for url in urls:
    soup = getWebsite(url)
    headlines = soup.find_all('div', class_ = 'assetText')

    for headline in headlines:
      if topic.lower() in headline.h3.get_text().lower():
        titles.append(headline.h3.get_text())
        subSoup = getWebsite("https://www.cnet.com" + headline.a.get('href'))
        articles.append("".join([x.get_text() for x in subSoup.find('div', class_ = 'article-main-body').find_all("p")]))

    if len(urls) < 2: #The number here indicates the number of pages in the website we want our program to crawl and scrap info(Max being 2000)
      urls.append("https://www.cnet.com" + soup.find('a', class_ = 'next').get('href'))

  urls = ["https://www.techradar.com/reviews"]

  soup = getWebsite(urls[0])
  pages = soup.find('ul', class_ = 'pagination-numerical-list').find_all('a')
  for page in pages:
    if len(urls) < 2:
      urls.append(page.get('href'))


  #urls = urls[:-1] #This part is written due to the structure of the website html

  for url in urls:
    soup = getWebsite(url)
    headlines = soup.find_all('div', class_ = 'listingResult')

    for headline in headlines:
      if headline.h3 is not None:
        if topic.lower() in headline.h3.get_text().lower():
          titles.append(headline.h3.get_text())
          subSoup = getWebsite(headline.a.get('href'))
          articles.append("".join([x.get_text() for x in subSoup.find(id = 'article-body').find_all("p")]))

  urls = ["https://www.tomsguide.com/reviews"]

  soup = getWebsite(urls[0])
  pages = soup.find('ul', class_ = 'pagination-numerical-list').find_all('a')
  for page in pages:
    if len(urls) < 2:
      urls.append(page.get('href'))

  #urls = urls[:-1]

  for url in urls:
    soup = getWebsite(url)
    headlines = soup.find_all('a', class_ = 'article-link')

    for headline in headlines:
      if topic.lower() in headline.h3.get_text().lower():
        titles.append(headline.h3.get_text())
        subSoup = getWebsite(headline.get('href'))
        articles.append("".join([x.get_text() for x in subSoup.find(id = 'article-body').find_all('p')]))

newsDict = {}
i = 0

for title in titles:
  newsDict[title] = articles[i]
  i += 1

if topic is not None:
  resp = {
      "Response":200,
      "articles":newsDict
  }
else:
  resp = {
      "Response":300
  }

print(json.dumps(resp))

sys.stdout.flush()
