import requests
from abc import abstractmethod
from app import app

class BaseAuthenticationProvider:
	@abstractmethod
	def constructAuthorizationCodeRequestUrl(self):
		return

	@abstractmethod
	def getAuthorizationCode(self, authorizationCodeRequestUrl):
		return

	@abstractmethod
	def constructAccessTokenRequestUrl(self, code):
		return

	@abstractmethod
	def getAccessToken(self, accessTokenRequestUrl):
		return

	@abstractmethod
	def constructServiceRequestUrl(self, accessToken):
		return

	@abstractmethod
	def getUserData(self):
		return

class GoogleAuthenticationProvider(BaseAuthenticationProvider):
	def constructAuthorizationCodeRequestUrl(self):
		baseUrl = 'https://accounts.google.com/o/oauth2/auth?'
		scope = 'email+profile'
		state = '/core'
		redirect_uri = 'http://localhost:5000/auth/oauth2/callback'
		response_type = 'code'
		constructedUrl = baseUrl + '&scope=' + scope + '&state=' + state + '&redirect_uri=' + redirect_uri + '&response_type=' + response_type + '&client_id=' + app.config['GOOGLE_CONSUMER_KEY']
		return constructedUrl

	def getAuthorizationCode(self, authorizationCodeRequestUrl):
		response = requests.post(authorizationCodeRequestUrl)
		return response

	def constructAccessTokenRequestUrl(self, code):
		baseUrl = 'https://www.googleapis.com/oauth2/v3/token?'
		redirect_uri= 'http://localhost:5000/auth/oauth2/access-token-callback'
		grant_type = 'authorization_code'
		constructedUrl = baseUrl + '&code=' + code + '&client_id' + app.config['GOOGLE_CONSUMER_KEY'] + '&client_secret' + 
		app.config['GOOGLE_CONSUMER_SECRET'] + '&redirect_uri' + redirect_uri + '&grant_type' + grant_type
		return constructedUrl

	def getAccessToken(self, accessTokenRequestUrl):
		response = requests.post(accessTokenRequestUrl)
		return response

	def constructServiceRequestUrl(self, accessToken):
		baseUrl = 'https://www.googleapis.com/plus/v1/people/me?'
		constructedUrl = baseUrl + '&access_token' + accessToken
		return constructedUrl

	def getUserData(self, serviceRequestUrl):
		response = request.post(serviceRequestUrl)
		return response