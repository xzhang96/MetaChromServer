import os
from flask import Flask, render_template, request
import time

app = Flask(__name__)
APP_ROOT = os.path.dirname(os.path.abspath(__file__))

@app.route('/')
def index():
    return render_template('homepage.html')


@app.route('/results', methods=['GET', 'POST'])
def get_info():
    if request.method == 'POST':
        fileType = request.form['fileType']
    return fileType

if __name__ == '__main__':
    app.run()
