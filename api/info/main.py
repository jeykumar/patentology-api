# INFO

from api.common.incoming import Request
from parse import Parser
from query import Query

def info_handler(arguments):
    payload = Request(arguments, endpoint='info').parse()
    url = Query(payload).generate_url()
    results = Parser(url)
    results_dict = results.parse()
    return results_dict