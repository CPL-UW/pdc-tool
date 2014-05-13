from flask import Flask
app = Flask(__name__)


'''	Target date, 5/15/2014
	TODO: Upload/Download functionality working
	TODO: Jazmyn gets function for csvfy
	TODO: Dennis gets function for keysums'''

@app.route('/')
def index():
    return 'Index Page'
    '''TODO: have the index page allow the upload of a json file. After succesful upload, select from list of available functions'''

@app.route('/analysis')
def analysis():
    return 'Choose the analysis to use on the current JSON file'
    '''choose analysis or upload a new file'''


@app.route('/Upload')
def upload():
    return 'Upload Page'
    
@app.route('/Output')
def output():
    return 'output Page'
    '''allows the download of the correct csv file'''
    
@app.route('/Csvfy')
def csvfy():
    return 'Upload Page'
    
@app.route('/keysums')
def keysums():
    return 'Upload Page'
    
@app.route('/register')
def register():
    return 'This is reg'

if __name__ == '__main__':
    app.run()

