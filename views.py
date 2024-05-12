import json
import logging
from flask import Blueprint, render_template, request, redirect, flash, url_for, session
from flask_login import login_required, login_user, logout_user, current_user
from werkzeug.security import check_password_hash
from query import *
from models import Fault_log, User
from datetime import datetime
from forms import DeviceLogForm, RegisterForm, LoginForm
import plotly.graph_objs as go
from plotly.utils import PlotlyJSONEncoder

# Creating blueprints for the application
floors_blueprint = Blueprint('floors', __name__)
rooms_blueprint = Blueprint('rooms', __name__)
devices_blueprint = Blueprint('devices', __name__)
fault_log_blueprint = Blueprint('fault_log', __name__)
graphs_blueprint = Blueprint('graphs', __name__)
users_blueprint = Blueprint('users', __name__)
index_blueprint = Blueprint('index', __name__)


# Register frame blueprint
@users_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    from app import db
    form = RegisterForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()

        if user:
            flash('Username address already exists')
            return render_template('register.html', form=form)

        new_user = User(username=form.username.data, password=form.password.data, role='admin')

        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('users.login'))


    return render_template('register.html', form=form)


# Login frame blueprint
@users_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    from app import db

    if not session.get('logins'):
        session['logins'] = 0
        # if login attempts is 3 or more create an error message
    elif session.get('logins') >= 3:
        flash('Number of incorrect logins exceeded')

    form = LoginForm()

    if form.validate_on_submit():

        session['logins'] += 1
        user = User.query.filter_by(username=form.username.data).first()

        if not user or not check_password_hash(user.password, form.password.data):
            if session['logins'] == 3:
                flash('Number of incorrect logins exceeded')
            elif session['logins'] == 2:
                flash('Please check your login details and try again. 1 login attempt remaining')
            else:
                flash('Please check your login details and try again. 2 login attempts remaining')

            return render_template('login.html', form=form)

        session['logins'] = 0

        login_user(user)

        user.last_logged_in = user.current_logged_in
        user.current_logged_in = datetime.now()
        db.session.commit()

        logging.warning('SECURITY - Log in [%s, %s, %s]', current_user.id, current_user.username, request.remote_addr)

        return index()

    return render_template('login.html', form=form)


# Logout Blueprint
@users_blueprint.route('/logout')
@login_required
def logout():
    logging.warning('SECURITY - Log out [%s, %s, %s]', current_user.id, current_user.username, request.remote_addr)
    logout_user()
    return redirect(url_for('users.login'))

@index_blueprint.route('/index', methods=['GET'])
@login_required
def index():
    month_data = query_month_data()
    print(month_data)
    # Implement the logic to render the index page (floors)
    return render_template('index.html')  # Assuming your index page is named 'index.html'



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


# Fault_log frame blueprint
@fault_log_blueprint.route('/fault_log', methods=['GET'])
def fault_log():
    fault_log_data = query_fault_log()
    return render_template('fault_log.html', fault_log_data=fault_log_data)


# Data visualisation frame blueprint
@graphs_blueprint.route('/graphs', methods=['GET'])
def graphs():
    fault_type_freq_data = query_fault_type_freq()

    fault_types = [row[0] for row in fault_type_freq_data]
    counts = [row[1] for row in fault_type_freq_data]

    bar_graph = go.Bar(
        x=fault_types,
        y=counts

    )

    bar_graph_json = json.dumps([bar_graph], cls=PlotlyJSONEncoder)

    floor_freq_data = query_floor_freq()

    labels = [row[0] for row in floor_freq_data]
    values = [row[1] for row in floor_freq_data]

    # Create Pie chart
    pie_chart = go.Figure(data=[go.Pie(labels=labels, values=values)])

    # Customize layout
    pie_chart.update_layout(title='Fault Floor Frequency')

    pie_chart_json = json.dumps(pie_chart, cls=PlotlyJSONEncoder)

    room_freq_data = query_room_freq()
    print(room_freq_data)
    room_name = [row[0] for row in room_freq_data]
    frequency = [row[1] for row in room_freq_data]
    # Create a histogram trace
    rooms_barchart = go.Bar(
        x=room_name,
        y=frequency,
    )

    # Create a layout for the histogram
    layout = go.Layout(
        title='Faults per Room',
        xaxis=dict(title='Room_Name'),
        yaxis=dict(title='Frequency'),

    )

    # Create a figure
    figure = go.Figure(data=[rooms_barchart], layout=layout)

    # Convert the figure to JSON
    histogram_json = json.dumps(figure, cls=PlotlyJSONEncoder)

    month_data = query_month_data()
    months = [row[0] for row in month_data]
    frequency = [row[1] for row in month_data]
    line_chart = go.Scatter(
        x=months,
        y=frequency,
        name='Faults per Month'
    )
    line_chart_json = json.dumps(line_chart, cls=PlotlyJSONEncoder)


    return render_template('graphs.html', bar_graph=bar_graph_json, pie_chart=pie_chart_json, histogram=histogram_json, line_chart=line_chart_json)
