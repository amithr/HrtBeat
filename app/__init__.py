# Import Flask, Blueprint, and controller-related libraries
from flask import Flask

# Define WSGI application object
app = Flask(__name__, static_path='/static')
app.config.from_object('config')

# Enables use of Angularjs in templates
from flask.ext.triangle import Triangle
Triangle(app)

# Import SQLAlchemy and related migration library
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.migrate import Migrate, MigrateCommand

# Script runner, used in models
from flask.ext.script import Manager

# Define the database, migration, and manager objects - all apply to models
db = SQLAlchemy(app)
migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)

# Import core module
from app.core.controllers import core

# Import provider module
from app.providers.controllers import providers

# Register blueprints
app.register_blueprint(core)
app.register_blueprint(providers)

