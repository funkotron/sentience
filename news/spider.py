from sentience.news.models import Entity,Article,Stock
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
                 chunk_size=50,
                 total_articles=1000):
        self.entity = entity
        self.start = start
        self.end = end
        self.chunk_size = chunk_size #How many results to return in one request
        self.total_articles = total_articles
        self.find_articles()
        self.grab_prices()
        return True

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

    def find_articles(self)
        #Return any article urls related to an entity between two given dates

        while True:
            url = "http://www.google.co.uk/finance/company_news?q=%s:%s&startdate=%s&enddate=%s&start=%d&num=%d"%(self.entity.exchange,
                  self.entity.ticker,
                  self.startdate.strftime("%Y-%m-%d"),
                  self.enddate.strftime("%Y-%m-%d"),
                  start_count,
                  self.chunk_size)
            html = urllib.urlopen(url).read()
            soup = BeautifulSoup.BeautifulSoup(html)
            article_list = soup.findAll("div", {"class":"g-section news sfe-break-bottom-16"})
            if not article_list:
                break
            for i in article_list:
                link = i.find("span",{"class":"name"}).a
                name = link.text
                url = link.attrs[0]
                date_text = i.find("span",{"class":"date"}).text
                date = datetime.strptime(date_text,"%b %d, %Y")
                src = i.find("span",{"class":"src"}).text
                body = self.get_visible(url)
                article = Article(name=name,
                                  entity=self.entity,
                                  src=src,
                                  date = date,
                                  body = body)
                article.save()


        return True

    def grab_prices(self)
        #Get stock prices
        url = urllib.urlencode("http://www.google.co.uk/finance/historical?q=%s:%s&startdate=%s&enddate=%s&output=csv" % (
              self.sentity.exchange,
              self.entity.ticker,
              self.start.strftime("%b+%d,+%Y"),
              self.end.strftime("%b+%d,+%Y")
        ))
        html = urllib.urlopen(url).read().split('\n')
        for row in html[1:]:
            fields = row.split(',')
            date = fields[0]
            price = fields[4]
            stock = Stock(date=date,
                               price=price,
                               entity=self.entity)
            stock.save()


        return True

