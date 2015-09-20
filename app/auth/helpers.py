import requests
from abc import abstractmethod
from flask import json
from app import db, app
from app.auth.models import User, Role
import hashlib
import uuid

'''Login, generate authorization token using access token, send to frontend, store in cookie'''
'''Pass authorization code back for each request, decrypt using decorator function'''
'''Authorization code should be in a cookie after the first login, destroy cookie every hour, force user to login again'''
'''Hold access token and login details in a session? Not sure - One app load pass the session key'''

class BaseAuthenticationProvider:
	@abstractmethod
	def constructAuthorizationCodeRequestUrl(self):
		return

	@abstractmethod
	def constructAccessTokenRequestUrl(self, code):
		return

	def getAccessToken(self, accessTokenRequestUrl):
		response = requests.post(accessTokenRequestUrl)
		decodedResponse = json.loads(response.content)
		return decodedResponse["access_token"]

	def storeAccessToken(self, accessToken):
		return True

	@abstractmethod
	def getUserData(self):
		return

	def processUserData(self, userData):
		user = User.query.filter_by(email=userData["email"]).first()
		if user is None:
			newUser = User(email = userData["email"], name = userData["name"], provider_id = userData["provider_id"], access_token = userData["access_token"])
			db.session.add(newUser)
			db.session.commit()
			return True
		return False

	@abstractmethod
	def logout(self):
		return


class GoogleAuthenticationProvider(BaseAuthenticationProvider):
	client_id = app.config['GOOGLE_CLIENT_ID']

	provider_id = 'google'

	client_secret = app.config['GOOGLE_CLIENT_SECRET']

	redirect_uri = 'http://localhost:5000/auth/oauth2/google/callback'

	def constructAuthorizationCodeRequestUrl(self):
		baseUrl = 'https://accounts.google.com/o/oauth2/auth?'
		scope = 'email+profile'
		state = '/core'
		response_type = 'code'
		constructedUrl = baseUrl + '&scope=' + scope + '&state=' + state + '&redirect_uri=' + self.redirect_uri + '&response_type=' + response_type + '&client_id=' + self.client_id
		return constructedUrl

	def constructAccessTokenRequestUrl(self, code):
		baseUrl = 'https://www.googleapis.com/oauth2/v3/token?'
		grant_type = 'authorization_code'
		constructedUrl = baseUrl + '&code=' + code + '&client_id=' + self.client_id + '&client_secret=' + self.client_secret + '&redirect_uri=' + self.redirect_uri + '&grant_type=' + grant_type
		return constructedUrl

	def getUserData(self, accessToken):
		userRequestUrl = 'https://www.googleapis.com/plus/v1/people/me'
		headers = {"Authorization": "Bearer " + accessToken}
		userResponse = requests.get(url = userRequestUrl, headers = headers)
		filteredUserResponse = self._filterUserResponse(userResponse)
		return filteredUserResponse

	def _filterUserResponse(self, userResponse):
		decodedResponse = json.loads(userResponse.content)
		userEmail = decodedResponse['emails'][0]['value']
		userName = decodedResponse['name']['givenName'] + ' ' + decodedResponse['name']['familyName']
		userData = {"email": userEmail, "name": userName}
		return userData

	def logout(self):
		return True


class FacebookAuthenticationProvider(BaseAuthenticationProvider):
	client_id = app.config['FACEBOOK_CLIENT_ID']

	provider_id = 'facebook'

	client_secret = app.config['FACEBOOK_CLIENT_SECRET']

	redirect_uri = 'http://localhost:5000/auth/oauth2/facebook/callback'

	def constructAuthorizationCodeRequestUrl(self):
		baseUrl = 'https://www.facebook.com/dialog/oauth?'
		response_type = 'code'
		scope = 'email,public_profile'
		constructedUrl = baseUrl + 'client_id=' + self.client_id + '&redirect_uri=' + self.redirect_uri + '&response_type=' + response_type  + '&scope=' + scope
		return constructedUrl

	def constructAccessTokenRequestUrl(self, code):
		baseUrl = 'https://graph.facebook.com/v2.3/oauth/access_token?'
		constructedUrl = baseUrl + 'client_id=' + self.client_id + '&redirect_uri=' + self.redirect_uri + '&client_secret=' + self.client_secret + '&code=' + code
		return constructedUrl

	def getUserData(self, accessToken):
		userRequestUrl = 'https://graph.facebook.com/me?fields=email,name&access_token=' + accessToken
		userResponse = requests.get(userRequestUrl)
		filteredUserResponse = self._filterUserResponse(userResponse)
		filteredUserResponse["access_token"] = accessToken
		return filteredUserResponse

	def _filterUserResponse(self, userResponse):
		decodedUserResponse = json.loads(userResponse.content)
		userData = {"email": decodedUserResponse["email"], "name": decodedUserResponse["name"], "provider_id": self.provider_id}
		return userData

	def logout(self):
		return True

class BaseCryptoProvider():
	def requires_authorization_token:
		@wraps(f)
		def decorated_function(*args, **kwargs):
			authorizationToken = flask.request.headers.get('Authorization-Token')
			if not authorizationToken:
				'''Login page'''
			else:
				'''Pass'''
		return decorated_function

	def hashStringValue(value):
		salt = uuid.uuid4().hex
    	return hashlib.sha256(salt.encode() + password.encode()).hexdigest() + ':' + salt

	def checkHashedStringAgainstOriginalString(hashedString, originalString):
		original, salt = hashedString.split(':')
    	return original == hashlib.sha256(salt.encode() + originalString.encode()).hexdigest())



