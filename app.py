from flask import Flask
from models import db
from config import Config
from populate import populate_data
from query import query_floors
from views import floors_blueprint, rooms_blueprint, devices_blueprint, fault_log_blueprint, graphs_blueprint


# Flask creation and configuration
app = Flask(__name__)
app.config.from_object(Config)
app.secret_key = Config.SECRET_KEY


# Initialise DB
db.init_app(app)


@app.route('/')
def DB_test():  # put application's code here
    return query_floors()


#Register blueprints
app.register_blueprint(floors_blueprint)
app.register_blueprint(rooms_blueprint)
app.register_blueprint(devices_blueprint)
app.register_blueprint(fault_log_blueprint)
app.register_blueprint(graphs_blueprint)

# Run application if executed as main script
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        #populate_data()
        app.run()

