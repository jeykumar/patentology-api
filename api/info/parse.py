# INFO

import lxml
import requests
from bs4 import BeautifulSoup
from urlparse import urljoin
from api.common.scraper import Scraper

BASE_URL = 'http://www.ic.gc.ca/'

class Parser(Scraper):
    def td_line(self, e):
        parts = []
        if not e:
            return u''
        for s in e.stripped_strings:
            parts.append(s)
        line = u' '.join(parts)
        return line
    
    def td_list(self, e):
        lines = []
        for li in e.find_all('li'):
            lines.append(self.td_line(li))
        return lines
    
    def parse_application(self, summary_table):
        application = u''
        application = self.td_line(summary_table.find('td', attrs={'headers':'patentNum'}).find('strong'))
        return application
        
    def parse_titles(self, summary_table):
        titles = {}
        titles['en'] = self.td_line(summary_table.find('td', attrs={'headers':'EnglishTitle'}))
        titles['fr'] = self.td_line(summary_table.find('td', attrs={'headers':'FrenchTitle'}))
        return titles
        
    def parse_bib(self, bib_div):
        bib_data = {}
        
        # Parse second table: 'patent details table'
        details_table = bib_div.find('table', attrs={'id':'patentDetailsTable'})
        if details_table:
            details_body = details_table.tbody
            for row in details_body.children:
                if row.name != 'tr':
                    # Skip non-header children (e.g. newlines)
                    continue
                # Should include some error handling below in case there is no 'th' or 'td'
                header = row.th['id']
                data = row.td
                
                # Process according to header
                if header == 'intlClass':
                    bib_data['ipc'] = self.td_list(data)
                elif header == 'canClass':
                    bib_data['cpc'] = self.td_list(data)
                elif header == 'inventors':
                    bib_data['inventors'] = self.td_list(data)
                elif header == 'owners':
                    bib_data['owners'] = self.td_list(data)
                elif header == 'applicants':
                    bib_data['applicants'] = self.td_list(data)
                elif header == 'agent':
                    bib_data['agent'] = self.td_line(data)
                elif header == 'issued':
                    bib_data['issued'] = self.td_line(data)
                elif header == 'filingDate':
                    bib_data['filing-date'] = self.td_line(data)
                elif header == 'pubDate':
                    bib_data['pub-date'] = self.td_line(data)
                elif header == 'lic':
                    bib_data['licence'] = self.td_line(data)
                elif header == 'lang':
                    bib_data['language'] = self.td_line(data)
                
        return bib_data
    
    def parse_abstracts(self, abstracts_div):
        abstracts = []
        paragraphs = abstracts_div.find_all('p')
        for para in paragraphs:
            parts = []
            for s in para.stripped_strings:
                s = u' '.join(s.split())
                parts.append(s)
            abstracts.append(u' '.join(parts))
        return abstracts
    
    def parse_claims(self, claims_div):
        claims = u''
        parts = []
        for s in claims_div.stripped_strings:
            s = u' '.join(s.split())
            parts.append(s)
        claims = (u' '.join(parts))
        return claims
    
    def parse_drawing(self, drawing_tab):
        if drawing_tab.find('img'):
            img_url_segment = drawing_tab.find('img').get('src')
            drawing = urljoin(BASE_URL, img_url_segment)
        else:
            drawing = u''
        return drawing
    
    def parse(self):
        html = self.get_html()
        soup = BeautifulSoup(html, 'lxml')
        
        results = {}
        
        # Check if patent was found
        summary_table = soup.find('table', attrs={'id':'patentSummaryTable'})
        if not summary_table:
            results['found'] = 'False'
            return results
        else:
            results['found'] = 'True'
        
        # Parse titles
        summary_table = soup.find('table', attrs={'id':'patentSummaryTable'})
        titles = self.parse_titles(summary_table)
        results['titles'] = titles
        
        # Parse application number
        summary_table = soup.find('table', attrs={'id':'patentSummaryTable'})
        application = self.parse_application(summary_table)
        results['application'] = application
        
        # Parse bibliographic data tab
        bib_div = soup.find('div', attrs={'id':'tabs1_1'})
        bib = self.parse_bib(bib_div)
        results['bibliographic-data'] = bib
        
        # Parse abstracts tab
        abstracts_div = soup.find('div', attrs={'id':'tabs1_2'})
        abstracts = self.parse_abstracts(abstracts_div)
        results['abstracts'] = abstracts
        
        # Parse claims tab
        claims_div = soup.find('div', attrs={'id':'tabs1_3'})
        claims = self.parse_claims(claims_div)
        results['claims'] = claims
        
        # Parse drawing tab
        drawing_tab = soup.find('div', attrs={'id':'tabs1_4'})
        drawing = self.parse_drawing(drawing_tab)
        results['drawing'] = drawing

        return results
            