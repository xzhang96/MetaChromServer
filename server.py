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


@app.route('/results', methods=['POST'])
def get_info():
    if request.method == 'POST':
        fileType = request.form['fileType']
        uploadMethod = request.form['inputFile']
        t = time.time()
        if uploadMethod == 'file':
            uploadFile = request.files['inputUploadFile']
            fileName = str(t) + '_' + fileType + '_' + uploadFile.filename
            uploadFile.save(os.path.join(UPLOAD_FOLDER, secure_filename(fileName)))
        elif uploadMethod == 'paste':
            uploadFile = request.form['inputTextFile']
            fileName = str(t) + '_' + fileType + '_textUpload'
            print(uploadFile, file=open(os.path.join(UPLOAD_FOLDER, secure_filename(fileName)), 'w'))

    return "file upload successfully!"

if __name__ == '__main__':
    app.run(debug = True)
