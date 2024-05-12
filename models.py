from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash
from flask_login import UserMixin
from datetime import datetime
from sqlalchemy.orm import relationship

db = SQLAlchemy()

# Defines User class
class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(100), nullable=False)
    registered_on = db.Column(db.DateTime, nullable=False)
    last_logged_in = db.Column(db.DateTime, nullable=True)
    current_logged_in = db.Column(db.DateTime, nullable=True)

    faults = relationship('Fault_log', backref='user', lazy=True)

    def __init__(self, username, password, role):
        self.username = username
        self.password = generate_password_hash(password)
        self.role = role
        self.registered_on = datetime.now()
        self.last_logged_in = None
        self.current_logged_in = None


# Define the Rooms class
class Rooms(db.Model):
    __tablename__ = 'rooms'

    room_id = db.Column(db.Integer, primary_key=True)
    room_name = db.Column(db.String(50))
    floor_name = db.Column(db.String(50))


# Define the Devices class
class Devices(db.Model):
    __tablename__ = 'devices'

    device_id = db.Column(db.Integer, primary_key=True)
    device_name = db.Column(db.String(50))
    room_id = db.Column(db.Integer, db.ForeignKey('rooms.room_id'))
    device_type = db.Column(db.String(50))


# Define Faults class
class Faults(db.Model):
    __tablename__ = 'faults'

    fault_id = db.Column(db.Integer, primary_key=True)
    fault_type = db.Column(db.String(50))
    fault_severity = db.Column(db.String(50))


# Define Fault_log class
class Fault_log(db.Model):
    __tablename__ = 'fault_log'

    fault_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    device_id = db.Column(db.Integer, db.ForeignKey('devices.device_id'))
    fault_type = db.Column(db.String, db.ForeignKey('faults.fault_type'))
    floor_name = db.Column(db.String, db.ForeignKey('rooms.floor_name'))
    room_name = db.Column(db.String, db.ForeignKey('rooms.room_name'))
    log_date = db.Column(db.String(50))
    log_time = db.Column(db.String(50))
    fault_severity = db.Column(db.String(50))
    fault_description = db.Column(db.String(50))
    logged_by = db.Column(db.String, db.ForeignKey('users.username'))


# Define Tasks class
class Tasks(db.Model):
    task_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    assigned_to = db.Column(db.String, db.ForeignKey('users.username'))
    task_description = db.Column(db.String(50))
    assigned_by = db.Column(db.String, db.ForeignKey('users.username'))
    deadline = db.Column(db.Date)