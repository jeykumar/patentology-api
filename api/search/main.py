# SEARCH

from api.common.incoming import Request
from query import Query
from parse import Parser

def search_handler(arguments):
    payload = Request(arguments, endpoint='search').parse()
    url = Query(payload).generate_url()
    results_dict = Parser(url).parse()
    return results_dict