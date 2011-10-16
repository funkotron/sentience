from sentience.news.models import Entity,Article,Stock
from sentience.news.html2text import extractFromURL
import nltk.classify.util
from nltk.classify import NaiveBayesClassifier
from django.conf import settings
import urllib
import BeautifulSoup
from datetime import datetime
from datetime import timedelta

class Spider():

    def __init__(self,
                 entity=None,
                 start=(datetime.now()-timedelta(days=60)).date(),
                 end=(datetime.now()-timedelta(days=30)).date(),
                 chunk_size=50,
                 total_articles=1000):
        self.entity = entity
        self.start = start
        self.end = end
        self.chunk_size = chunk_size #How many results to return in one request
        self.total_articles = total_articles

    def find_articles(self):
        #Return any article urls related to an entity between two given dates

        start_count = 0
        while True:
            url = "http://www.google.co.uk/finance/company_news?q=%s:%s&startdate=%s&enddate=%s&start=%d&num=%d"%(
                  self.entity.exchange,
                  self.entity.ticker,
                  self.start.strftime("%Y-%m-%d"),
                  self.end.strftime("%Y-%m-%d"),
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
                print link.attrs[0][1]
                url = link.attrs[0][1]
                date_text = i.find("span",{"class":"date"}).text
                try:
                    date = datetime.strptime(date_text,"%b %d, %Y").date()
                except:
                    date = datetime.today().date()
                src = i.find("span",{"class":"src"}).text
                try:
                    body = extractFromURL(url,cache=True)
                except:
                    continue
                article = Article(name=name,
                                  entity=self.entity,
                                  src=src,
                                  date = date,
                                  body = body)
                article.save()
            start_count += self.chunk_size


        return True

    def grab_prices(self):
        #Get stock prices
        url = ("http://www.google.co.uk/finance/historical?q=%s:%s&startdate=%s&enddate=%s&output=csv" % (
              self.entity.exchange,
              self.entity.ticker,
              (self.start-timedelta(days=getattr(settings,'STOCK_DATE_RANGE',5))).strftime("%Y-%m-%d"),
              (self.end+timedelta(days=getattr(settings,'STOCK_DATE_RANGE',5))).strftime("%Y-%m-%d")
        ))
        html = urllib.urlopen(url).read().split('\n')
        for row in html[1:]:
            fields = row.split(',')
            if not fields[0]:
                continue
            date = datetime.strptime(fields[0],"%d-%b-%y")
            price = int(fields[4].replace('.',''))
            stock = Stock(date=date,
                               price=price,
                               entity=self.entity)
            stock.save()


        return True

    def label(self):
        #Mark the articles positive or negative depending on the trend of stock prices around the
        #date the article was published.

        articles = Article.objects.filter(entity=self.entity)

        for article in articles:
            date = article.date
            date_range_length = getattr(settings,'STOCK_DATE_RANGE',5)

            def differential(start):
                average = 0
                for i in range(0,date_range_length-1):
                    day = start + timedelta(days=i)
                    try:
                        stock = Stock.objects.filter(entity=self.entity).filter(date=day)[0]
                    except Exception, e:
                        print e
                        continue
                    average += stock.price
                return float(average) / date_range_length

            article.score = differential(date)
            article.save()

    def classify(self):
        #Classify

        articles = Article.objects.filter(entity=self.entity)

        def word_feats(body):
            words = body.split(' ')
            return dict([(word, True) for word in words])

        negids = articles.filter(score__lt=0)
        posids = articles.filter(score__gt=0)

        negfeats = [(word_feats(a.body), 'neg') for a in negids]
        posfeats = [(word_feats(a.body), 'pos') for a in posids]

        negcutoff = len(negfeats)*3/4
        poscutoff = len(posfeats)*3/4

        trainfeats = negfeats[:negcutoff] + posfeats[:poscutoff]
        testfeats = negfeats[negcutoff:] + posfeats[poscutoff:]
        print 'train on %d instances, test on %d instances' % (len(trainfeats), len(testfeats))

        classifier = NaiveBayesClassifier.train(trainfeats)
        print 'accuracy:', nltk.classify.util.accuracy(classifier, testfeats)
        classifier.show_most_informative_features()

    def run(self):
        self.grab_prices()
        self.find_articles()
        self.label()
        self.classify()
        return True

e = Entity.objects.all()
if e:
    e=e[0]
else:
    e = Entity(name="Google",ticker="GOOG",exchange="NASDAQ")
    e.save()
spider = Spider(entity=e)
#spider.classify()
spider.run()
