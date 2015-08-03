from flask import Blueprint, request, render_template, jsonify
from flask_security import auth_token_required, current_user, logout_user
from app.auth.models import User, Role
from app.core.models import Link, LinkList, Subscriber
from app import db, userDatastore, app

auth = Blueprint('auth', __name__, url_prefix='/auth')

@auth.route('/create/user', methods=['POST'])
@auth_token_required
def createUser():
	ret_dict = {
        "Key1": "Value1",
        "Key2": "value2"
    }
	return jsonify(items=ret_dict)

@auth.route('/retrieve/user', methods=['POST'])
def retrieveUser():
	return str(current_user.id)

@auth.route('/update/user', methods=['POST'])
def updateUser():
	return

@auth.route('/delete/user', methods=['POST'])
def deleteUser():
	return

@auth.route('/logout', methods=['POST'])
def logoutUser():
	logout_user();
	return jsonify(status=True)