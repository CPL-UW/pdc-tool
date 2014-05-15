import os
from flask import Flask, request, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename

'''
	Copyright 2014, CPL
	This script was written and maintained by Dennis Ramirez (@dennisRamirez), Jazmyn Russell
	This script is provided as is with no other guarantees.
	Please comment code.
'''

UPLOAD_FOLDER = './uploads/'
ALLOWED_EXTENSIONS = set(['json','txt'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

'''	Target date, 5/15/2014
	TODO: Upload/Download functionality working
	TODO: Jazmyn gets function for csvfy
	TODO: Dennis gets function for keysums'''

@app.route('/')
def index():
	#print url_for('analysis')
	return 'Index Page <a href="/upload">UPLOAD</a>'
	'''TODO: have the index page allow the upload of a json file. After succesful upload, select from list of available functions'''

#NOTE: commented out to avoid namespace collision
#@app.route('/analysis')
#def analysis():
#    return 'Choose the analysis to use on the current JSON file <div class="button"><a href="/csvfy">CSVFY</a></div>'
#    '''choose analysis or upload a new file'''

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/analysis/<filename>')
def analysis(filename):
    return 'Choose the analysis to use on the current JSON file <a href="'+url_for('csvfy', filename= filename)+'"> CSVFY</a>'
    '''choose analysis or upload a new file'''

@app.route('/upload', methods=['GET', 'POST'])
def upload():
	if request.method == 'POST':
		file = request.files['file']
		if file and allowed_file(file.filename):
			filename = secure_filename(file.filename)
			print(os.path.join(app.config['UPLOAD_FOLDER']))
			file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
			return redirect(url_for('analysis', filename= filename))
	return '''
	<!doctype html>
	<title>Upload new File</title>
	<h1>Upload new File</h1>
	<form action="" method=post enctype=multipart/form-data>
	<p><input type=file name=file>
	<input type=submit value=Upload></p>
	</form>
    '''
    
@app.route('/output/<filename>')
def output(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)
    '''allows the download of the correct csv file'''
    
@app.route('/csvfy/<filename>')
def csvfy(filename):
	f = send_from_directory(app.config['UPLOAD_FOLDER'], filename)
	# TODO: actually csvfy the file
	return f
    
@app.route('/keysums')
def keysums():
    return 'Upload Page'
    
@app.route('/register')
def register():
    return 'This is reg'

if __name__ == '__main__':
    app.run(debug=True)

