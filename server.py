import os
from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
import time

app = Flask(__name__)
APP_ROOT = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(APP_ROOT, 'InputData/')

@app.route('/')
def index():
    return render_template('homepage.html')


@app.route('/results', methods=['GET', 'POST'])
def get_info():
    if request.method == 'POST':
        fileType = request.form['fileType']
        uploadMethod = request.form['inputFile']
        if uploadMethod == 'file':
            uploadFile = request.files['inputUploadFile']
            # uploadFile.save(secure_filename(uploadFile.filename))
            t = time.time()
            fileName = str(t) + '_' + fileType + '_' + uploadFile.filename
            uploadFile.save(os.path.join(UPLOAD_FOLDER, fileName))


    return "file uploaded successfully"

if __name__ == '__main__':
    app.run(debug = True)
