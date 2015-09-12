from flask import Blueprint, request, render_template, jsonify
from flask_security import auth_token_required, current_user, logout_user
from app.auth.models import User, Role
from app.auth.helpers import GoogleAuthenticationProvider
from app.core.models import Link, LinkList, Subscriber
from app import db, userDatastore, app

auth = Blueprint('auth', __name__, url_prefix='/auth')

@auth.route('/create/login/user', methods=['POST'])
@auth_token_required
def createOrLoginUser():
	ret_dict = {
        "Key1": "Value1",
        "Key2": "value2"
    }
	return jsonify(items=ret_dict)

@auth.route('/request/access-key', methods=['POST', 'GET'])
def requestApiAccessKey():
	requestUrl = GoogleAuthenticationProvider().constructAuthorizationCodeRequestUrl()
	GoogleAuthenticationProvider().getAuthorizationCode(requestUrl)
	return str(requestUrl)

@auth.route('/oauth2/callback', methods=['POST', 'GET'])
def receiveAuthorizationCode():
	code = request.args.get('code')
	requestUrl = GoogleAuthenticationProvider().constructAccessTokenRequestUrl(code)
	response = GoogleAuthenticationProvider().getAccessToken(requestUrl)
	return str(response.content)

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