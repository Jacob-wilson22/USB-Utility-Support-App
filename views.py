from flask import Blueprint, render_template, request
from flask_login import current_user
from query import *
from models import Fault_log
from datetime import datetime
from forms import DeviceLogForm




floors_blueprint = Blueprint('floors', __name__)
rooms_blueprint = Blueprint('rooms', __name__)
devices_blueprint = Blueprint('devices', __name__)

# Floor selection frame blueprint
@floors_blueprint.route('/floors', methods=['GET'])
def floors():
    floor_data = query_floors()
    return render_template('floors.html', floor_data=floor_data)


# Room Selection frame blueprint
@rooms_blueprint.route('/rooms/<floor_name>', methods=['GET'])
def rooms(floor_name):
    room_data = query_rooms(floor_name)
    return render_template('rooms.html', room_data=room_data)


# Device selection frame blueprint
@devices_blueprint.route('/devices/<room_id>', methods=['GET', 'POST'])
def devices(room_id):
    from app import db
    fault_data = query_faults()
    form = DeviceLogForm(request.form)
    form.fault_type.choices = [(fault[1]) for fault in fault_data]
    floor_name = query_floor_name(room_id)
    room_name = query_room_name(room_id)
    floor_name = str(floor_name).strip()
    room_name = str(room_name).strip()

    if request.method == 'POST' and form.validate_on_submit():
        device_id = request.form['device_id']
        fault_type = form.fault_type.data
        fault_severity = form.fault_severity.data
        fault_description = form.fault_description.data
        log_date = datetime.now().strftime('%Y-%m-%d')
        log_time = datetime.now().strftime('%H:%M:%S')


        new_fault = Fault_log(
            device_id=device_id,
            fault_type=fault_type,
            floor_name=floor_name,
            room_name=room_name,
            fault_severity=fault_severity,
            fault_description=fault_description,
            log_date=log_date,
            log_time=log_time,


        )

        db.session.add(new_fault)
        db.session.commit()



    device_data = query_devices(room_id)


    return render_template('devices.html', device_data=device_data, form=form)