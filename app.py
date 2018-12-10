# -*- coding: utf-8 -*-
"""
    :author: Grey Li (李辉)
    :url: http://greyli.com
    :copyright: © 2018 Grey Li
    :license: MIT, see LICENSE for more details.
"""
import os
import uuid

from flask import Flask, render_template, flash, redirect, url_for, request, send_from_directory, session
from flask_wtf.csrf import validate_csrf
from wtforms import ValidationError
from form import CheckHashForm
from cictro_hash import Keccak

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'm1z0r3_f0r_fun')
app.jinja_env.trim_blocks = True
app.jinja_env.lstrip_blocks = True
flag = ""
with open('flag') as f:
    flag = f.read()

# Custom config
app.config['UPLOAD_PATH'] = os.path.join(app.root_path, 'uploads')
app.config['ALLOWED_EXTENSIONS'] = ['png', 'jpg', 'jpeg', 'gif']

# Flask config
# set request body's max length
# app.config['MAX_CONTENT_LENGTH'] = 3 * 1024 * 1024  # 3Mb



@app.route('/', methods=['GET', 'POST'])
def index():
    form = CheckHashForm()
    if request.method == 'POST':
        hash_1 = request.form.get('Hash_1')
        hash_2 = request.form.get('Hash_2')
        hash_1 = Keccak(hash_1).hex()
        hash_2 = Keccak(hash_2).hex()
        if hash_1 == hash_2:
            print(flag)
        
    return render_template('bootstrap.html',form=form)


