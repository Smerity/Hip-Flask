from flask import Flask
from flaskext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object("config.Development")
db = SQLAlchemy(app)
from models import Todo

@app.route("/")
def index():
  return "Hello world " + Todo.__tablename__ + " and DEBUG = " + str(app.config["DEBUG"]) + " and SQL = " + app.config["SQLALCHEMY_DATABASE_URI"]
