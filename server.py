import os
from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
import time
import pathlib
import re
import torch
import json
from numpyencoder import NumpyEncoder

app = Flask(__name__)
APP_ROOT = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(APP_ROOT, 'inputData/')
RESULT_FOLDER = os.path.join(APP_ROOT, 'results/')
app.config['UPLOAD_EXT'] = ['.txt', '.vcf']


@app.route('/')
@app.route('/homepage')
def index():
    return render_template('homepage.html')


@app.route('/result', methods=['POST'])
def get_info():
    t = time.time()
    error = None
    jobTitle = request.form['jobTitle']
    fileType = request.form['fileType']
    uploadMethod = request.form['inputFile']

    if len(jobTitle) != 0:
        jobTitle = str(t) + '_' + jobTitle
    else:
        jobTitle = str(t) + '_job'
    new_dir = pathlib.Path(UPLOAD_FOLDER, jobTitle)

    # Input file is variant data
    if fileType == 'var':
        if uploadMethod == 'file':
            uploadFile = request.files['inputUploadFile']
            filename = secure_filename(uploadFile.filename)
            if filename != "":
                file_ext = os.path.splitext(filename)[1]
                if file_ext not in app.config['UPLOAD_EXT']:
                    error = "File type not allowed!"
                    return render_template('homepage.html', error=error)
                else:
                    new_dir.mkdir(parents=True, exist_ok=True)
                    uploadFile.save(new_dir / 'input.txt')
            else:
                error = "Upload file not found!"
                return render_template('homepage.html', error=error)
        elif uploadMethod == 'paste':
            uploadFile = request.form['inputTextFile']
            if validate_var_paste_text(uploadFile, request.form['selectVar']):
                new_dir.mkdir(parents=True, exist_ok=True)
                new_file = new_dir / 'input.txt'
                new_file.write_text(uploadFile)
            else:
                error = "Paste text format error"
                return render_template('homepage.html', error=error)
        result_dir = pathlib.Path(RESULT_FOLDER, jobTitle)
        # render_template('loader.html')
        status = process_var_data(jobTitle, request.form['selectVar'], str(new_dir), result_dir)
        if status != None:
            return render_template('homepage.html', error=status)

    # Input file is FASTA file
    elif fileType == 'seq':
        pass
    return get_result(jobTitle)


def process_var_data(job_title, var_file_type, itm_dir, result_dir):
    dpCommand = ('python3 src/data_processing/SNP2Seq.py --InputType ' +
                 var_file_type + ' --InputFile inputData/' +
                 job_title + '/input.txt --OutDir ' + itm_dir +
                 ' --ToolDir tools/')
    dp_status = os.system(dpCommand)
    if (dp_status != 0):
        return "Detect error when processing input data!"
    result_dir.mkdir(parents=True, exist_ok=True)
    inferCommand = ('python3 src/infer_var.py --Model trained_model/' +
                    'MetaChrom/MetaFeat_ResNet --InputFile inputData/' +
                    job_title + '/out.vseq --OutDir ' + str(result_dir) +
                    ' --NumTarget 31')
    infer_status = os.system(inferCommand)
    if (infer_status != 0):
        return "Detect error when running inference!"
    
    return


def validate_var_paste_text(input, var_type):
    if len(input) == 0:
        return False
    else:
        ls = input.strip().split('\n')
        if var_type == 'VCF':
            for var in ls:
                return len(var.split('\t')) == 5
        elif var_type == 'rsid':
            for var in ls:
                return var[:2].lower() == 'rs' and len(var.split()) == 1
        else:
            return False


@app.route('/result')
def get_result(job_title):
    # job_title = '1600380155.8117108_job'
    result_path = os.path.join(RESULT_FOLDER, job_title)
    input_path = os.path.join(UPLOAD_FOLDER, job_title)
    result = torch.load(str(result_path)+'/results.pt')
    
    cell_type_31 = {'Glut': 0, 'CP': 1, 'DN': 2, 'FB_OCR': 3,
                 'GA': 4, 'GZ': 5, 'FB_H3K27ac': 6, 'iPS': 7,
                 'NPC': 8, 'ACC_neuron': 9, 'AMY_neuron': 10, 'DLPFC_neuron': 11,
                 'HIPP_neuron': 12, 'INS_neuron': 13, 'ITC_neuron': 14, 'MDT_neuron': 15,
                 'NAC_neuron': 16, 'OFC_neuron': 17, 'PMC_neuron': 18, 'PUT_neuron': 19,
                 'PVC_neuron': 20, 'STC_neuron': 21, 'VLPFC_neuron': 22, 'PEC_Enhancers':23,
                 'PEC_OCR':24, 'Organoid_0':25, 'Organoid_11':26, 'Organoid_30':27, 'PFC_H3K27ac':28,
                 'TC_H3K27ac':29, 'CBC_H3K27ac':30}
    content = dict()
    for item in result.items():
        abs_diff = []
        for num in item[1].get('abs_diff'):
            num = "{:.3e}".format(num)
            abs_diff.append(num)
        content[item[0]] = abs_diff
    
    unmatch = []
    if os.path.isfile(os.path.join(input_path, 'unmatch.txt')):
        unmatch_file = open(os.path.join(input_path, 'unmatch.txt'), 'r')
        for line in unmatch_file:
            unmatch.append(line.strip())

    cleanupCommand = 'rm -R ' + input_path
    os.system(cleanupCommand)
    return render_template('result.html', result=content,
                           cell_type=cell_type_31, unmatch=unmatch)


if __name__ == '__main__':
    app.run(debug=True, port=5050)
