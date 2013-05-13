# This is a program which
# writes images to a file. The images come from
# all Web pages that can be reached by a given URL
# by following up to a maximum of 3 hyperlinks.
# Only the first 100 hyperlinks are traversed.

from urllib.request import *
from urllib.error import URLError
from codecs import *
from urllib.parse import urljoin
from html.parser import HTMLParser
import socket

class Collector(HTMLParser):
    'collects hyperlink URLs into a list'

    def __init__(self, url):
        'initializes parser, the url, and a list'
        HTMLParser.__init__(self)
        self.url = url
        self.links = []
        self.images = []

    def handle_starttag(self, tag, attrs):
        'collects hyperlink and image URLs in their absolute format'
        if tag == 'a':
            for attr in attrs:
                if attr[0] == 'href':
                    # construct absolute URL
                    absolute = urljoin(self.url, attr[1])
                    if absolute[:4] == 'http': # collect HTTP URLs
                        self.links.append(absolute)
        if tag == 'img':
            for attr in attrs:
                if attr[0] == 'src':
                    # construct absolute URL
                    absolute = urljoin(self.url, attr[1])
                    if absolute[:4] == 'http': # collect HTTP URLs
                        self.images.append(absolute)
       
                        
    def getLinks(self):
        'returns hyperlinks URLs in their absolute format'
        return self.links

    def getImages(self):
        'returns image URLs in their absolute format'
        return self.images
        
class Crawler:
    def __init__(self, maxlinks=1):
        self.maxlinks = maxlinks
        self.links = [ ]
        self.images = [ ]
        self.counter = 0

    def crawl(self, url, level=0):
        if url not in self.links:
            try:
                if level == self.maxlinks:
                    return

                self.counter += 1
                print('Visiting URL {} {}'.format(self.counter, url))
                self.links.append(url)
                resource = urlopen(url, timeout=1)
                content = resource.read().decode()
                collector = Collector(url)
                collector.feed(content)
         
                
                for i in collector.getImages():
                    if i not in self.images:
                        self.images.append(i)


                for link in collector.getLinks():
                    if len(self.links) <= 100:
                     self.crawl(link, level+1)
            except ValueError:
                pass
            except URLError:
                pass
            except socket.timeout:
                pass
            except UnicodeError:
                pass
            return self.images
        

            

    def getImages(self):
        return self.images

    def getLinks(self):
        return self.links
        
def go(url, file='images.html', maxlinks=2):
    cwlr = Crawler(maxlinks)
    cwlr.crawl(url)

    html = open(file, 'w')
    html.write('<html>\n<head>\nHomework 5\n</head><body>\n')

    for i in cwlr.images:
        html.write('<img src="'+str(i)+'">')

    html.write('</body>\n</html>\n')
    html.close
   
