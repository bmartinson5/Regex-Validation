from flask import Flask, request
import flask
import regex
import sys
sys.path.append('/usr/local/lib/python3.6/site-packages')
from flask_cors import CORS
app = Flask(__name__)


cors = CORS(app, resources={r"/*": {"origins": "*"}})

@app.route('/')
def startApp():
    return flask.render_template('home.html')

@app.route('/findMatches', methods=["Post"])
def findMatches():
    req = request.get_json()

    pattern = req['pattern']
    stringToMatch = req['stringToMatch']

    result = regex.regexV(pattern, stringToMatch)

    return flask.jsonify(result = result)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
