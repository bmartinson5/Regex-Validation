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
    print(pattern, stringToMatch)
    wordsToCheck = stringToMatch.split(' ')
    result = []
    for word in wordsToCheck:
        longestMatch = []
        rangeList = []
        for i in range(0, len(word)):
            for x in range(i, len(word)):
                if regex.regexV(pattern, word[i:x+1]):
                    print(word[i:x+1])
                    print(i)
                    print(x+1)
                    longestMatch = [i, x+1]

                else:
                    if len(longestMatch) != 0:
                        rangeList.append(longestMatch)
                        longestMatch = []
                        i = x+1

        result.append(rangeList)

    print(result)
    #return the list of ranges for matches found in string
    return flask.jsonify(result = result)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
