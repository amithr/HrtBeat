from flask import Blueprint, request, render_template, jsonify, redirect, session, json
from flask_security import auth_token_required, current_user, logout_user
from app.auth.helpers import BaseAuthenticationProvider

auth = Blueprint('auth', __name__, url_prefix='/auth')

@auth.route('/request/access-key/<provider>', methods=['GET'])
def requestApiAccessKey(provider):
	providerObject = BaseAuthenticationProvider().getProviderObject(provider)
	requestUrl = providerObject.constructAuthorizationCodeRequestUrl()
	return redirect(requestUrl)

@auth.route('/oauth2/<provider>/callback', methods=['POST', 'GET'])
def receiveAuthorizationCode(provider):
	code = request.args.get('code')
	providerObject = BaseAuthenticationProvider().getProviderObject(provider)
	requestUrl = providerObject.constructAccessTokenRequestUrl(code)
	accessToken = providerObject.getAccessToken(requestUrl)
	userData = providerObject.getUserData(accessToken)
	providerObject.processUserData(userData);
	redirectUrl = '/core/' + userData["email"]
	return redirect(redirectUrl)

@auth.route('/retrieve/user', methods=['POST'])
def retrieveUser():
	data = request.get_json()
	userData = session[data["email"]]
	return userData

@auth.route('/update/user', methods=['POST'])
def updateUser():
	return

@auth.route('/delete/user', methods=['POST'])
def deleteUser():
	return

@auth.route('/logout/', methods=['POST'])
def logoutUser():
	data = request.get_json()
	provider = data["provider"]
	email = data["email"]
	providerObject = BaseAuthenticationProvider().getProviderObject(provider)
	providerObject.logout(email)
	return jsonify(status=True)