from flask import Flask, request, jsonify, abort, redirect, url_for, render_template, Response, send_file
import joblib
import pandas as pd
import numpy as np
from flask_wtf.file import FileField, FileRequired
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)

SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY

knn = joblib.load('iris_model.pkl')

@app.route('/user/<username>')
def show_user_profile(username):
    # show the user profile for that user    
    return 'User %s' % (float(username) * float(username))

@app.route('/iris/<param>')
def iris(param):
    param = param.split(',') 

    param = [float(n) for n in param]
    param = np.array(param).reshape(1, -1)

    predict = knn.predict(param)

    src = '<img src="/static/{}.jpg" width="480" height="480">'

    if predict[0] == 1:
        return src.format('setosa')
    elif predict[0] == 2:
        return src.format('versicolor')
    else:
        return src.format('virginica')

@app.route('/iris_post', methods=['POST'])
def add_message():
    try:
        content = request.get_json()

        param = content['flower'].split(',') 

        param = [float(n) for n in param]
        param = np.array(param).reshape(1, -1)

        predict = knn.predict(param)

        return jsonify({'class': str(predict[0])})

    except:
        return redirect(url_for('bad_request'))

@app.route('/badrequest400')
def bad_request():
    abort(400)

from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired

class MyForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()])
    file = FileField()

@app.route('/submit', methods=('GET', 'POST'))
def submit():
    form = MyForm()
    if form.validate_on_submit():
        f = form.file.data

        filename = form.name.data + '.csv'

        df = pd.read_csv(f, header=None)

        predict = knn.predict(df)

        result = pd.DataFrame(predict, columns=['class'])
        result.to_csv(filename, index=False)

        return send_file(filename,
                     mimetype='text/csv',
                     attachment_filename=filename,
                     as_attachment=True)

    return render_template('submit.html', form=form)

import os
from flask import Flask, flash, request, redirect, url_for
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = ''
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'csv', 'png', 'jpg', 'jpeg', 'gif'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename + '_uploaded')
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return('uploaded')
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''