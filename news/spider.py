import re
import urllib
import BeautifulSoup
from datetime import datetime
import timedelta

class Spider():

    def __init__(self, 
                 entity=None, 
                 start=datetime.now()-timedelta(days=60), 
                 end=datetime.now()):
        self.entity = entity
        self.start = start
        self.end = end

    def get_visible(url):
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

    def find_articles(entity,start,end):
        #Return any article urls related to an entity between two given dates
        return None


