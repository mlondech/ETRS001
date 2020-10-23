#! /usr/bin/python
# -*- coding:utf-8 -*-

from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///configuration.db'
app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
db = SQLAlchemy(app)

admin = Admin(app, name='Configuration', template_mode='bootstrap3')

Hardware_Monitoredobject = db.Table('Hardware_Monitoredobject',
    db.Column('hardware_id', db.Integer, db.ForeignKey('hardware.id'), primary_key=True),
    db.Column('monitoredobject_id', db.Integer, db.ForeignKey('monitoredobject.id'), primary_key=True)
)

class Monitoredobject(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True, nullable=False)
    oid = db.Column(db.String(255), nullable=True)
    
    def __repr__(self):
        return '<Monitored Object %r>' % self.name


class Hardware(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True, nullable=False)
    description = db.Column(db.String(255), unique=True, nullable=True)
    IPAddress = db.Column(db.String(255), unique=True, nullable=False)
    IPmask = db.Column(db.String(255), nullable=False)
    ports = db.Column(db.Integer, nullable=True)
    community = db.Column(db.String(255), nullable=False)

    monitoredobjects = db.relationship('Monitoredobject', secondary=Hardware_Monitoredobject, lazy='subquery',
    backref=db.backref('hardwares', lazy=True))

    def __repr__(self):
        return '<Hardware %r>' % self.name

admin.add_view(ModelView(Monitoredobject, db.session))
admin.add_view(ModelView(Hardware, db.session))

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