import lxml
from urllib import request

def getScore(symbol):
    url = f"https://feeds.finance.yahoo.com/rss/2.0/headline?s=AAPL&region=US&lang=en-US"
    xmlData = request.urlretrieve(url)