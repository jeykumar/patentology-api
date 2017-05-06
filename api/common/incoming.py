class Request(object):
    def __init__(self, request, endpoint=''):
        self.arguments = request
        self.endpoint = endpoint
        self.payload = {}
    def parse(self):
        payload = {}
        for i in self.arguments:
            payload[i] = self.arguments[i]
        # Validate arguments and error handling here.
        # TO DO
        return payload