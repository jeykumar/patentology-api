#!flask/bin/python
from flask import Flask
from flask import request
from flask import jsonify
from Call import Call
from Query import Query
from Results import Results
from Reply import Reply

app = Flask(__name__)

@app.route('/')
def index():
    return "Hello, World!"

    
@app.route('/v1/search', methods=['GET'])
def search():
    arguments = request.args
    payload = Call(arguments).parse()
    url = Query(payload).url()
    results = Results(url).results()
    reply_dict = Reply(results).reply_dict()
    return jsonify(reply_dict)
    
if __name__ == '__main__':
    app.run(debug=True)