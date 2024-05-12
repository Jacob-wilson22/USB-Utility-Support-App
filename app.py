from flask import Flask, redirect, url_for
from flask_login import LoginManager
from config import Config
from models import db, User
from populate import populate_data
from views import floors_blueprint, rooms_blueprint, devices_blueprint, fault_log_blueprint,\
    graphs_blueprint, users_blueprint, index_blueprint


# Flask creation and configuration
app = Flask(__name__)
app.config.from_object(Config)
app.secret_key = Config.SECRET_KEY


# Initialise DB
db.init_app(app)


# Initialise login manager
login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.init_app(app)


# User loader function for login manager
@login_manager.user_loader
def load_user(id):
        return User.query.get(int(id))


# Route for login page
@app.route('/')
def index():
    return redirect(url_for('users.login'))


# Register blueprints
app.register_blueprint(floors_blueprint)
app.register_blueprint(rooms_blueprint)
app.register_blueprint(devices_blueprint)
app.register_blueprint(fault_log_blueprint)
app.register_blueprint(graphs_blueprint)
app.register_blueprint(users_blueprint)
app.register_blueprint(index_blueprint)

# Run application if executed as main script
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        #populate_data()
        app.run()

