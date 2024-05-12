# config.py
# Establishes DB URI and secret key.
class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///Diss.db'
    SECRET_KEY = 'your_secret_key'