# SEARCH

class Query(object):    
    def __init__(self, payload={}):
        self.payload = payload
        
    def parse_payload(self):
        self.id = self.payload['id']   
        
    def generate_url(self):
        self.parse_payload()
        url_en = "http://www.ic.gc.ca/opic-cipo/cpd/eng/patent/{}/summary.html".format(self.id)
        url_fr = "http://www.ic.gc.ca/opic-cipo/cpd/fra/brevet/{}/sommaire.html".format(self.id)
        url = {'en': url_en, 'fr': url_fr}
        return url['en']
