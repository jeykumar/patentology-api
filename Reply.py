from json import dumps

class Reply(object):
    def __init__(self, results):
        self.count = results[0]
        self.limit_exceeded = results[1]
        self.patents = results[2]
        self.reply = None
    def reply_dict(self):
        reply_dict = {'count':self.count, 'limit_exceeded':str(self.limit_exceeded), 'patents':[]}
        for p in self.patents:
            d = {'number':p[0], 'title':p[1], 'link':p[2]}
            reply_dict['patents'].append(d)
        return reply_dict
    def json_reply(self):
        reply_dict = self.compile_reply_dict()
        json_reply = dumps(reply_dict)
        self.reply = json_reply
        return self.reply
    def pretty_json(self):
        reply_dict = self.compile_reply_dict()
        print jdumps(reply_dict, sort_keys=True, indent=4, separators=(',', ': '))