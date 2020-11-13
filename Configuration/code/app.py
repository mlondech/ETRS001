#! /usr/bin/python
# -*- coding:utf-8 -*-

from flask import Flask, render_template, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from marshmallow_sqlalchemy.fields import Nested

app = Flask(__name__)
app.config['SECRET_KEY'] = 'ggdwkjfceflekcsdcicoslek,c'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///configuration.db'
app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
db = SQLAlchemy(app)
ma = Marshmallow(app)
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

    monitoredobjects = db.relationship('Monitoredobject', secondary=Hardware_Monitoredobject,
                                        lazy='subquery',backref=db.backref('hardwares', lazy=True))

    def __repr__(self):
        return '<Hardware %r>' % self.name

class MonitoredobjectSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Monitoredobject

class HardwareSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Hardware
        include_relationships = True
    monitoredobjects = Nested(MonitoredobjectSchema, many=True)

admin.add_view(ModelView(Monitoredobject, db.session))
admin.add_view(ModelView(Hardware, db.session))
monitoredobjects_schema = MonitoredobjectSchema()
hardwares_schema = HardwareSchema(many=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/json')
def config():
    hardwares = Hardware.query.all()
    return jsonify(hardwares_schema.dump(hardwares))

if __name__ == '__main__':
    app.run()