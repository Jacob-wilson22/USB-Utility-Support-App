from flask import Flask
from models import db
from config import Config
from populate import populate_data
from query import query_floors


# Flask creation and configuration
app = Flask(__name__)
app.config.from_object(Config)
app.secret_key = Config.SECRET_KEY


# Initialise DB
db.init_app(app)


@app.route('/')
def DB_test():  # put application's code here
    return query_floors()

# Run application if executed as main script
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        populate_data()
        app.run()

