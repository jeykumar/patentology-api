from urllib import quote_plus
from constants import *

class Query(object):    
    def __init__(self, payload={}):
        self.payload = payload
        self.search_strings = {
            'Any Text Field':[],
            'Title':[],
            'Abstract':[],
            'Claims':[],
            'Inventor':[],
            'Owners':[],
            'Applicant':[],
            'IPC':[],
            'CPC':[],
            'PCT Filing No.':[],
            'Intl Pub No.':[]
        }
        
        self.parameters = {
            'Inventor Country':None,
            'Status':None,
            'Type':None,
            'Language':None,
            'License Availability':None,
            'Date Search':None, 
            'Date Start':None,  # yyyy-mm-dd
            'Date End':None     # yyyy-mm-dd
        }
    
    def parse_payload(self):
        # Parse search strings
        payload = self.payload
        keyword = payload.get('keyword')
        if keyword:
            self.search_strings['Any Text Field'] = [keyword]
            
        title = payload.get('title')
        if title:
            self.search_strings['Title'] = [title]
            
        abstract = payload.get('abstract')
        if abstract:
            self.search_strings['Abstract'] = [abstract]
            
        claims = payload.get('claims')
        if claims:
            self.search_strings['Claims'] = [claims]
            
        inventor = payload.get('inventor')
        if inventor:
            self.search_strings['Inventor'] = [inventor]
            
        owner = payload.get('owner')
        if owner:
            self.search_strings['Owners'] = [owner]
            
        applicant = payload.get('applicant')
        if applicant:
            self.search_strings['Applicant'] = [applicant]
            
        ipc = payload.get('ipc')
        if ipc:
            self.search_strings['IPC'] = [ipc]
            
        cpc = payload.get('cpc')
        if cpc:
            self.search_strings['CPC'] = [cpc]
            
        pct = payload.get('pct')
        if pct:
            self.search_strings['PCT Filing No.'] = [pct]
            
        ipn = payload.get('ipn')
        if ipn:
            self.search_strings['Intl Pub No.'] = [ipn]
        
        # Parse parameters
        country = payload.get('country')
        if country:
            self.parameters['Inventor Country'] = country

        status = payload.get('status')
        if status:
            self.parameters['Status'] = status

        type = payload.get('type')
        if type:
            self.parameters['Type'] = type

        language = payload.get('language')
        if language:
            self.parameters['Language'] = language

        licence_filter = payload.get('licence-filter')
        if licence_filter:
            self.parameters['License Availability'] = licence_filter

        date_field = payload.get('date-field')
        if date_field:
            self.parameters['Date Search'] = date_field

        date_start = payload.get('date-start')
        if date_start:
            self.parameters['Date Start'] = date_start

        date_end = payload.get('date-end')
        if date_end:
            self.parameters['Date End'] = date_end

            
        
    def parse_text_field(self, text_field, value):
        search_string_segment = ''
        if text_field == 'Any Text Field':
            search_string_segment = ' <AND> '.join(["({})".format(i) for i in value])
        elif text_field == 'Title':
            search_string_segment = '(({}) <IN> TITLE)'.format(','.join(value))
        elif text_field == 'Abstract':
            search_string_segment = '(({}) <IN> ABSTRACT)'.format(','.join(value))
        elif text_field == 'Claims':
            search_string_segment = '(({}) <IN> CLAIMS)'.format(','.join(value))
        elif text_field == 'Inventor':
            search_string_segment = '(({}) <IN> INVENTOR)'.format(','.join(value))
        elif text_field == 'Owners':
            search_string_segment = '(({}) <IN> OWNER)'.format(','.join(value))
        elif text_field == 'Applicant':
            search_string_segment = '(({}) <IN> APPLICANT)'.format(','.join(value))    
        elif text_field == 'IPC':
            search_string_segment = '(({}) <IN> IPC)'.format(','.join(value))      
        elif text_field == 'CPC':
            search_string_segment = '(({}) <IN> CPC)'.format(','.join(value))
        elif text_field == 'PCT Filing No.':
            search_string_segment = '(({}) <IN> PCTNUM)'.format(','.join(value))
        elif text_field == 'Intl Pub No.':
            search_string_segment = '(({}) <IN> INTNUM)'.format(','.join(value))    
        return search_string_segment
    
    def parse_parameter(self, parameter, value):
        parameter_segment = ''
        
        if parameter == 'Inventor Country': #INCOMPLETE!!
            if value == 'Inventor Country Not Selected':
                pass
            else:
                country_code = COUNTRIES.get(value)
                parameter_segment += '({} <IN> INVTCOUNTRY)'.format(country_code)
            
        if parameter == 'Status':
            if value == 'All':
                pass
            elif value == 'Active':
                parameter_segment += '(Active <IN> STATUS)'
            elif value == 'Patents':
                parameter_segment += '(Patents <IN> STATUS)'
            elif value == 'Pending Applications':
                parameter_segment += '(Pending Applications <IN> STATUS)'
            elif value == 'Public Domain':
                parameter_segment += '(Public Domain <IN> STATUS)'
                
        if parameter == 'Type':
            if value == 'All Documents':
                pass
            elif value == 'PCT':
                parameter_segment += '(Y <IN> PCT)'
            elif value == 'Non-PCT':
                parameter_segment += '((<NOT> Y) <IN> PCT)'
        
        if parameter == 'Language':
            if value == 'In Both Languages':
                pass
            elif value == 'English':
                parameter_segment += '(EN <IN> LANGUAGE)'
            elif value == 'French':
                parameter_segment += '(FR <IN> LANGUAGE)'

        if parameter == 'License Availability':
            if value == 'No':
                pass
            elif value == 'Yes':
                parameter_segment += '(Y <IN> LICENSE)'
                
        if parameter == 'Date Search':
            if value == 'Date Search Not Active':
                pass
            else:
                date_start = self.parameters['Date Start']
                date_end = self.parameters['Date End']
                if value == 'Issue Date':
                    parameter_segment += '(ISD>={}) <AND> (ISD<={})'.format(date_start, date_end)
                elif value == 'Filing Date':
                    parameter_segment += '(APD>={}) <AND> (APD<={})'.format(date_start, date_end)
                elif value == 'Examination Request Date':
                    parameter_segment += '(ERD>={}) <AND> (ERD<={})'.format(date_start, date_end)
                elif value == 'Open To Pub. Insp. Date':
                    parameter_segment += '(LOD>={}) <AND> (LOD<={})'.format(date_start, date_end)
                elif value == 'Priority Date':
                    parameter_segment += '(PAPD>={}) <AND> (PAPD<={})'.format(date_start, date_end)
                elif value == 'National Entry Date':
                    parameter_segment += '(NED>={}) <AND> (NED<={})'.format(date_start, date_end)
        
        return parameter_segment
                
        
    def url(self):
        self.parse_payload()
        search_string = ''
        for key in FIELDS['TEXT_FIELDS']:
            value = self.search_strings[key]
            if value != []:
                if search_string:
                    search_string += " <AND> "
                search_string += self.parse_text_field(key, value)
                
        parameters_ordered = [
            'Inventor Country',
            'Status',
            'Type',
            'Language',
            'License Availability',
            'Date Search'
        ]
        for key in parameters_ordered:
            value = self.parameters[key]
            if value != None:
                if search_string:
                    search_string += " <AND> "
                search_string += self.parse_parameter(key, value)
                
                
        safe = '<>'
        base = 'http://www.ic.gc.ca/opic-cipo/cpd/eng/search/results.html?query='
        end = '&start=1&num=50&type=advanced_search&newSearch=0'
        
        mid = quote_plus(search_string, safe=safe)
        q = base + mid + end
        return q
