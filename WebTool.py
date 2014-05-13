from flask import Flask
app = Flask(__name__)

@app.route('/')
def index():
    return 'Index Page'
    '''TODO: have the index page allow the upload of a json file. After succesful'''

@app.route('/hello')
def hello():
    return 'Hello World'

if __name__ == '__main__':
    app.run()

