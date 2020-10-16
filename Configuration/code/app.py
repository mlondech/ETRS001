#! /usr/bin/python
# -*- coding:utf-8 -*-

from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from models import db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////configuration.db'
db.init_app(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/config.html')
def config():
    return render_template('config.html')

@app.route('/surv.html')
def surv():
    return render_template('surv.html')


if __name__ == '__main__':
    app.run()