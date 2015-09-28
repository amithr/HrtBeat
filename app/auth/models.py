from app import db, manager, migrate
from app.core.models import LinkList
from flask.ext.security import Security, SQLAlchemyUserDatastore, \
    UserMixin, RoleMixin, login_required

# Define models
roles_users = db.Table('roles_users',
        db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
        db.Column('role_id', db.Integer(), db.ForeignKey('role.id')))

link_lists_users = db.Table('link_lists_users', 
        db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
        db.Column('link_list_id', db.Integer(), db.ForeignKey('link_list.id')))

class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True)
    name = db.Column(db.String(255))
    access_token = db.Column(db.String(255))
    provider = db.Column(db.String(255))
    image_url = db.Column(db.String(512))
    active = db.Column(db.Boolean())
    confirmed_at = db.Column(db.DateTime())
    last_login_at = db.Column(db.DateTime())
    current_login_at = db.Column(db.DateTime())
    last_login_ip = db.Column(db.String(45))
    current_login_ip = db.Column(db.String(45))
    login_count = db.Column(db.Integer)
    admin_link_lists = db.relationship('LinkList', backref='user')
    editor_link_lists = db.relationship('LinkList', secondary=link_lists_users, backref=db.backref('users', lazy='dynamic'))
    roles = db.relationship('Role', secondary=roles_users,
                            backref=db.backref('users', lazy='dynamic'))