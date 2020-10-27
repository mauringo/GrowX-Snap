from flask import Flask, redirect, render_template, request, session, url_for
from werkzeug.utils import secure_filename as a

import os 
dir_path = os.path.dirname(os.path.realpath(__file__))
print(dir_path+"/uploads")
app = Flask(__name__, static_url_path='')




os.chdir(dir_path)



@app.route('/', methods=['GET', 'POST'])
def index():    
    return render_template('index.html')
	
@app.route('/howtostart', methods=['GET', 'POST'])
def howtostart():
	return render_template('howtostart.html')

@app.route('/settings', methods=['GET', 'POST'])
def home():
	return render_template('settings.html')  

@app.route('/about', methods=['GET', 'POST'])
def about():
	return render_template('about.html')  

if __name__ == '__main__':
   app.run(host='0.0.0.0',debug = True)
