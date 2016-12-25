class Call(object):
    def __init__(self, request):
        self.arguments = request
        self.payload = {}
    def parse(self):
        payload = {}
        for i in self.arguments:
            payload[i] = self.arguments[i]
        # Validate arguments and error handling here.
        # TO DO
        return payload