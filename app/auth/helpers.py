import requests
from abc import abstractmethod
from app import app
from flask import json

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

	@abstractmethod
	def getUserData(self):
		return

class GoogleAuthenticationProvider(BaseAuthenticationProvider):
	client_id = app.config['GOOGLE_CLIENT_ID']

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
		userResponse = requests.get(url = serviceRequestUrl, headers = headers)
		filteredUserResponse = filterUserResponse(userResponse)
		return filterUserResponse

	def filterUserResponse(userResponse):
		decodedResponse = json.loads(userResponse.content)
		userEmail = decodedResponse['email'][0]
		userName = decodedResponse['name']['givenName'] + ' ' + decodedResponse['name']['familyName']
		userData = {"email": userEmail, "name": userName}
		return userData


class FacebookAuthenticationProvider(BaseAuthenticationProvider):
	client_id = app.config['FACEBOOK_CLIENT_ID']

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
		decodedUserResponse = json.loads(userIdResponse.content)
		return decodedUserResponse

	def filterUserResponse(userResponse):
		decodedUserResponse = json.loads(userResponse.content)
		userData = {"email": decodedUserResponse["email"], "name": decodedUserResponse["name"]}
		return userData