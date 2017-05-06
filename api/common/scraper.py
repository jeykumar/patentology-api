import requests

class Scraper(object):
    def __init__(self, url=''):
        self.url = url
    def get_html(self):
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10.6; en-US; rv:1.9.2.11) Gecko/20101012 Firefox/3.6.11'}
        req = requests.get(self.url, headers=headers)
        html = req.content
        return html