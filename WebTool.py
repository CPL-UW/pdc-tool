import os, time, datetime
from adageParseFunctions import getKeySums, getKeySumsByPlayer, toCSV, getCSV, plotVar, plotVars, getKeys
from flask import Flask, request, redirect, url_for, send_from_directory, render_template
from werkzeug.utils import secure_filename

'''
	Copyright 2014, CPL
	This script was written and maintained by Dennis Ramirez (@dennisRamirez), Jazmyn Russell
	This script is provided as is with no other guarantees.
	Please comment code.
'''

UPLOAD_FOLDER = './uploads/'
OUTPUT_FOLDER = './outputs/'
ALLOWED_EXTENSIONS = set(['json','txt'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER

@app.route('/')
def index():
	#print url_for('analysis')
	return render_template('index.html')
	
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
    return render_template('analysis.html', filename = filename)

@app.route('/upload', methods=['GET', 'POST'])
def upload():
	if request.method == 'POST':
		file = request.files['file']
		if file and allowed_file(file.filename):
			filename = secure_filename(file.filename)
			print(os.path.join(app.config['UPLOAD_FOLDER']))
			file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
			return redirect(url_for('analysis', filename= filename))
	return render_template('upload.html')
    
@app.route('/output/<filename>')
def output(filename):
    return send_from_directory(app.config['OUTPUT_FOLDER'], filename)
    '''allows the download of the correct csv file'''
    
@app.route('/csvfy/<filename>')
def csvfy(filename):
	out = getCSV(filename)
	oName = str(time.mktime(datetime.datetime.now().timetuple()))+'.csv'
	toCSV(oName, out)
	title = "Json -> CSV"
	message = "Json has been converted to CSV"
	return render_template('generalout.html',title = title, message = message, imagePath = "", outputFilename = oName, filename = filename)

@app.route('/plotvariable/<filename>', methods=['GET', 'POST'])
def plotvariable(filename):
	title = "Plotting Variable over time"
	if request.method == 'POST':
		key = request.form['keyword']
		oName = plotVar(filename,key)
		message = key+" X timestamp"
		return render_template('generalout.html',title = title, message = message, imagePath = oName, outputFilename = oName, filename = filename)
	else:
		message = "Choose variable to plot"
		keys = getKeys(filename)
		return render_template('getplotdata.html', title = title, message = message, keys = keys, twoVars = False);
	#oName = str(time.mktime(datetime.datetime.now().timetuple()))+'.csv'
	#toCSV(oName, out)
	
 
@app.route('/plotvariables/<filename>', methods=['GET', 'POST'])
def plotvariables(filename):
	title = "Plotting Variables"
	if request.method == 'POST':
		key = request.form['keyword']
		key2 = request.form['keyword2']
		oName = plotVars(filename,key,key2)
		message = key+" X " +key2
		return render_template('generalout.html',title = title, message = message, imagePath = oName, outputFilename = oName, filename = filename)
	else:
		message = "Choose variables to plot"
		keys = getKeys(filename)
		return render_template('getplotdata.html', title = title, message = message, keys = keys, twoVars = True);
 
@app.route('/keysums/<filename>')
def keysums(filename):
	out = getKeySums(filename)
	oName = str(time.mktime(datetime.datetime.now().timetuple()))+'.csv'
	toCSV(oName, out)
	title = "Unique Keys and Counts"
	message = out
	return render_template('generalout.html',title = title, message = message, imagePath = "", outputFilename = oName, filename = filename)

@app.route('/keysumsbyplayer/<filename>')
def keysumsbyplayer(filename):
	#f = send_from_directory(app.config['UPLOAD_FOLDER'], filename)
	out = getKeySumsByPlayer(filename)
	oName = str(time.mktime(datetime.datetime.now().timetuple()))+'.csv'
	toCSV(oName, out)
	title = "Unique Keys and counts by player"
	message = out
	return render_template('generalout.html',title = title, message = message, imagePath = "", outputFilename = oName, filename = filename)
	
@app.route('/register')
def register():
    return 'This is reg'

if __name__ == '__main__':
    app.run(debug=True)

