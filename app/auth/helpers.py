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

	@abstractmethod
	def getAccessToken(self, accessTokenRequestUrl):
		return

	def storeAccessToken(self, accessToken):
		return

	@abstractmethod
	def constructServiceRequestUrl(self, accessToken):
		return

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

	def getAccessToken(self, accessTokenRequestUrl):
		response = requests.post(accessTokenRequestUrl)
		print decodedResponse
		decodedResponse = json.load(response.content)
		return decodedResponse["access_token"]

	def storeAccessToken(self, accessToken):
		return

	def constructServiceRequestUrl(self, accessToken):
		baseUrl = 'https://www.googleapis.com/plus/v1/people/me?'
		constructedUrl = baseUrl + '&access_token=' + accessToken
		return constructedUrl

	def getUserData(self, serviceRequestUrl):
		response = requests.post(serviceRequestUrl)
		return response

class FacebookAuthenticationProvider(BaseAuthenticationProvider):
	client_id = app.config['FACEBOOK_CLIENT_ID']

	client_secret = app.config['FACEBOOK_CLIENT_SECRET']

	redirect_uri = 'http://localhost:5000/auth/oauth2/facebook/callback'

	def constructAuthorizationCodeRequestUrl(self):
		baseUrl = 'https://www.facebook.com/dialog/oauth?'
		response_type = 'code'
		constructedUrl = baseUrl + 'client_id=' + self.client_id + '&redirect_uri=' + self.redirect_uri + '&response_type=' + response_type 
		return constructedUrl

	def constructAccessTokenRequestUrl(self, code):
		baseUrl = 'https://graph.facebook.com/v2.3/oauth/access_token?'
		constructedUrl = baseUrl + 'client_id=' + self.client_id + '&redirect_uri=' + self.redirect_uri + '&client_secret=' + self.client_secret + '&code=' + code
		return constructedUrl

	def getAccessToken(self, accessTokenRequestUrl):
		response = requests.post(accessTokenRequestUrl)
		return response

	def storeAccessToken(self, accessToken):
		return

	def constructServiceRequestUrl(self, accessToken):
		return

	def getUserData(self, serviceRequestUrl):
		return