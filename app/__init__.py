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

# Setup security
from app.auth.models import User, Role
from flask.ext.security import Security, SQLAlchemyUserDatastore
userDatastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, userDatastore)

# Setup queueing system
from celery import Celery
celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)

# Import core module
from app.core.controllers import core

# Import provider module
from app.providers.controllers import providers

# Import authentication/security module
from app.auth.controllers import auth

# Register blueprints
app.register_blueprint(core)
app.register_blueprint(providers)
app.register_blueprint(auth)