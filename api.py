from flask import Flask
app = Flask(__name__)

@app.route('/')
def startApp():
    return flask.render_template('home.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
