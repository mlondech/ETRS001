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


if __name__ == '__main__':
    app.run()