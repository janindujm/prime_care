from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate


app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'  # Change this to a random string
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://u2skrhg1d6886h:p23c27b00706f8e8cca77b5636f827f95d8f0f3efdf19dd7c73df4b5571600f65@c5p86clmevrg5s.cluster-czrs8kj4isg7.us-east-1.rds.amazonaws.com:5432/d4knjj07rf4pcf'
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

migrate = Migrate(app,db)

from app import routes, models
