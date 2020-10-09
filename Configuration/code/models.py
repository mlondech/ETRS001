from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

Hardware_MonitoredObject = db.Table('Hardware_MonitoredObject',
    db.Column('hardware_id', db.Integer, db.ForeignKey('hardware.id'), primary_key=True),
    db.Column('monitoredObject_id', db.Integer, db.ForeignKey('monitoredobject.id'), primary_key=True)
)

MonitoredObject_Group = db.Table('MonitoredObject_Group',
    db.Column('monitoredObject_id', db.Integer, db.ForeignKey('monitoredobject.id'), primary_key=True),
    db.Column('group_id', db.Integer, db.ForeignKey('group.id'), primary_key=True)
)

Group_Hardware = db.Table('Group_Hardware',
    db.Column('group_id', db.Integer, db.ForeignKey('group.id'), primary_key=True),
    db.Column('hardware_id', db.Integer, db.ForeignKey('hardware.id'), primary_key=True)
)

class Hardware(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True, nullable=False)
    IPAddress = db.Column(db.String(255), unique=True, nullable=False)
    IPmask = db.Column(db.String(255), nullable=False)
    ports = db.Column(db.Integer, nullable=True)
    community = db.Column(db.String(255), nullable=False)

    monitoredObjects = db.relationship('MonitoredObject', secondary=Hardware_MonitoredObject, lazy='subquery',
        backref=db.backref('hardwares', lazy=True))

    groups = db.relationship('Groups', secondary=Group_Hardware, lazy='subquery',
        backref=db.backref('hardwares', lazy=True))

    def __repr__(self):
        return '<Hardware %r>' % self.username

class MonitoredObject(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True, nullable=False)
    oid = db.Column(db.String(255), unique=True, nullable=False)

    monitoredObjects = db.relationship('MonitoredObject', secondary=MonitoredObject_Group, lazy='subquery',
        backref=db.backref('group', lazy=True))

    def __repr__(self):
        return '<Monitored Object %r>' % self.name

class Group(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True, nullable=False)

    def __repr__(self):
        return '<Group %r>' % self.name