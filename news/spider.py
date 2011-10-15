from sentience.news.models import Entity,Article
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

    def find_articles(self)
        #Return any article urls related to an entity between two given dates
        url = "http://www.google.co.uk/finance/company_news?q=%s:%s&start=%d&num=%d"%(self.entity.exchange,
                                                                                      self.entity.ticker,
                                                                                      start_count,
                                                                                      self.chunk_size)
        html = urllib.urlopen(url).read()
        soup = BeautifulSoup.BeautifulSoup(html)
        #TODO iterate over this
        article_list = soup.findAll("div", {"class":"g-section news sfe-break-bottom-16"})
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


