from flask import Flask
from flask import render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask import redirect

from backend.models import *

app = None #Flask(__name__)

def init_app():
    house_helper = Flask(__name__)
    house_helper.debug = True
    
    house_helper.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///house_helper.sqlite3"
    house_helper.app_context().push()
    db.init_app(house_helper)
    print("house_helper application started ...")
    return house_helper

app = init_app()

from backend.controllers import *


if __name__ == "__main__":
    app.run(debug = True)



