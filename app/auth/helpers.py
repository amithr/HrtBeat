import requests
from abc import abstractmethod
from app import app

class BaseAuthenticationProvider:
	client_id = app.config['GOOGLE_CONSUMER_KEY']
	client_secret = app.config['GOOGLE_CONSUMER_SECRET']

	@abstractmethod
	def constructAuthorizationCodeRequestUrl(self, clientId):
		return

	@abstractmethod
	def getAuthorizationCode(self, requestUrl):
		return

	@abstractmethod
	def constructAccessTokenRequestUrl(self, code, clientId, clientSecret):

	@abstractmethod
	def validateAccessToken(self, token):
		return

	@abstractmethod
	def getUserData(self):
		return

class GoogleAuthenticationProvider(BaseAuthenticationProvider):
	def constructRequestUrl(self, client_id):
		baseUrl = 'https://accounts.google.com/o/oauth2/auth?'
		scope = 'email+profile'
		state = '/core'
		redirect_uri = 'http://localhost:5000/auth/oauth2/callback'
		response_type = 'code'
		constructedUrl = baseUrl + '&scope=' + scope + '&state=' + state + '&redirect_uri=' + redirect_uri + '&response_type=' + response_type + '&client_id=' + self.client_id
		return constructedUrl

	def getAccessToken(self, requestUrl):
		response = requests.post(requestUrl)
		return response

	def constructAccessTokenRequestUrl(self, code)

	def validateAccessToken(self, token):
		requestUrl = 'https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=' + token;
		response = request.post(requestUrl)

	def getUserData(self):
		requestUrl = ''
		response = request.post(requestUrl)
		return response