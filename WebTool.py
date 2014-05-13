import os
from flask import Flask, request, redirect, url_for
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = '/uploads'
ALLOWED_EXTENSIONS = set(['json'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

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


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['GET', 'POST'])
def upload():
	if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('uploaded_file',
                                    filename=filename))
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form action="" method=post enctype=multipart/form-data>
      <p><input type=file name=file>
         <input type=submit value=Upload>
    </form>
    '''
    
@app.route('/output/<filename>')
def output(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)
    '''allows the download of the correct csv file'''
    
@app.route('/csvfy')
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

