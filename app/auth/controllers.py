from flask import Blueprint, request, render_template, jsonify, redirect
from flask_security import auth_token_required, current_user, logout_user
from app.auth.helpers import BaseAuthenticationProvider

auth = Blueprint('auth', __name__, url_prefix='/auth')

@auth.route('/create/login/user', methods=['POST'])
@auth_token_required
def createOrLoginUser():
	ret_dict = {
        "Key1": "Value1",
        "Key2": "value2"
    }
	return jsonify(items=ret_dict)



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
	userData["is_user_new"] = providerObject.processUserData(userData)
	return render_template('app.html', userData = userData)

@auth.route('/retrieve/user', methods=['POST'])
def retrieveUser():
	return str(current_user.id)

@auth.route('/update/user', methods=['POST'])
def updateUser():
	return

@auth.route('/delete/user', methods=['POST'])
def deleteUser():
	return

@auth.route('/logout/<provider>', methods=['POST'])
def logoutUser():
	providerObject = BaseAuthenticationProvider().getProviderObject(provider)
	providerObject.logout()
	return jsonify(status=True)