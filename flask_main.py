from flask import Flask, request, jsonify, render_template, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os, requests, json
# from flask_api import api, db
from flask_api import api
from models import db
from flask_site import site
from flask_site import Site
from flask_api import Api


class Main:
    app = Flask(__name__)
    basedir = os.path.abspath(os.path.dirname(__file__))
    app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'

    # Update HOST and PASSWORD appropriately.
    HOST = "35.189.26.40"
    USER = "root"
    PASSWORD = "xiaoyu"
    DATABASE = "SmartLibrary"

    app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://{}:{}@{}/{}".format(USER, PASSWORD, HOST, DATABASE)
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True

    db.init_app(app)

    app.register_blueprint(api)
    app.register_blueprint(site)

    Api()
    Site()


if __name__ == "__main__":
    main = Main()
    main.app.run(host="0.0.0.0")
    # app.run(host = "0.0.0.0")
