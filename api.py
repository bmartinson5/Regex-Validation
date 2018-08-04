from flask import Flask, request
import flask
import regex
import check
import sys
sys.path.append('/usr/local/lib/python3.6/site-packages')
from flask_cors import CORS
app = Flask(__name__)


cors = CORS(app, resources={r"/*": {"origins": "*"}})

@app.route('/')
def startApp():
    return flask.render_template('home.html')

@app.route('/checkLegalRegex', methods=["Post"])
def checkRegex():
    req = request.get_json()
    patternToCheck = req['pattern']
    result = check.checkV(patternToCheck)
    return flask.jsonify(result=result)

@app.route('/findMatches', methods=["Post"])
def findMatches():
    req = request.get_json()
    pattern = req['pattern']
    stringToMatch = req['stringToMatch']
    wordsToCheck = stringToMatch.split(' ')
    result = []
    for word in wordsToCheck:
        longestMatch = []
        rangeList = []
        for i in range(0, len(word)):
            for x in range(i, len(word)):
                if regex.regexV(pattern, word[i:x+1]):
                    longestMatch = [i, x+1]

                else:
                    if len(longestMatch) != 0:
                        rangeList.append(longestMatch)
                        longestMatch = []
                        i = x+1

        result.append(rangeList)

    #return the list of ranges for matches found in string
    return flask.jsonify(result = result)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
