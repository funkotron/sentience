from sentience.news.models import StockPrice
import re
import urllib
import BeautifulSoup
from datetime import datetime
import timedelta

class Spider():

    def __init__(self, 
                 entity=None, 
                 start=datetime.now()-timedelta(days=60), 
                 end=datetime.now(),
                 chunk_size = 50):
        self.date_range = []
        days = (end - start).days()
        for i in range(days):
            self.date_range.append(
        self.end = end
        self.chunk_size = chunk_size #How many results to return in one request

    def get_visible(self,url):
        #Return the visible text on a page
        #Adapted from http://stackoverflow.com/questions/1936466/beautifulsoup-grab-visible-webpage-text
        html = urllib.urlopen(url).read()
        soup = BeautifulSoup.BeautifulSoup(html)
        texts = soup.findAll(text=True)

        def visible(element):
            if element.parent.name in ['style', 'script', '[document]', 'head', 'title']:
                return False
            elif re.match('.*<!--.*-->.*', str(element), re.DOTALL):
                return False
            return True

        visible_texts = filter(visible, texts)
        return visible_texts

    def grab_prices(self)
        #Return any article urls related to an entity between two given dates
        url = "http://www.google.co.uk/finance/historical?cid=694653&startdate=Oct+16%2C+2005&enddate=Oct+15%2C+2011&output=csv"
                                                                                      self.entity.ticker,
                                                                                      start_count,
                                                                                      self.chunk_size)
        html = urllib.urlopen(url).read().split('\n')
        for row in html[1:]:
            fields = row.split(',')
            date = fields[0]
            price = fields[4]
            stock = StockPrice(date=date,
                               price=price,
                               entity=self.entity)


        return True


