from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand
from app import app, db, migrate, manager
from app.core.models import LinkList, Link, Subscriber
from app.auth.models import User

if __name__ == '__main__':
	manager.run()