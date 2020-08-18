import os
from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
import time
import pathlib

app = Flask(__name__)
APP_ROOT = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(APP_ROOT, 'InputData/')

@app.route('/')
def index():
    return render_template('homepage.html')


@app.route('/results', methods=['POST'])
def get_info():
    if request.method == 'POST':
        t = time.time()
        jobTitle = request.form['jobTitle']
        if len(jobTitle) != 0:
            jobTitle = str(t) + '_' + jobTitle
        else:
            jobTitle = str(t) + '_job'
        new_dir = pathlib.Path(UPLOAD_FOLDER, jobTitle)
        new_dir.mkdir(parents=True, exist_ok=True)
        fileType = request.form['fileType']
        uploadMethod = request.form['inputFile']
        
        if uploadMethod == 'file':
            uploadFile = request.files['inputUploadFile']
            uploadFile.save(new_dir / 'input.txt')
        elif uploadMethod == 'paste':
            uploadFile = request.form['inputTextFile']
            new_file = new_dir / 'input.txt'
            new_file.write_text(uploadFile)

    return "file upload successfully!"

if __name__ == '__main__':
    app.run(debug = True)
