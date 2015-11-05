from abc import abstractmethod
from app import mail, app, celery
from flask.ext.mail import Message
import traceback
import os
import youtube_dl

class DownloadError(Exception):
	def __init__(self, value):
		self.value = value
	def __str__(self):
		return repr(self.value)

class BaseMediaProvider:
	localDownloadsDirectory = 'app/static/downloads'

	sender = app.config['MAIL_USERNAME']

	userEmail = ''

	def __init__(self, userEmail):
		self.userEmail = userEmail

	def downloadSong(self, url, artist, title):
		ydl_opts = {
			'format': 'bestaudio/best',
			'outtmpl': 'app/static/downloads/%(id)s.%(ext)s',
			'postprocessors': [{
				'key': 'FFmpegExtractAudio',
				'preferredcodec': 'mp3',
				'preferredquality': '192'
			}]
		}

		with youtube_dl.YoutubeDL(ydl_opts) as ydl:
			try:
				print "%s already downloaded, continuing..."
				result = ydl.extract_info(url, download=False)
				self.sendEmailWithDownload.delay(self.getLocalDownloadPath(result['id']), self.userEmail, self.sender)
			except OSError:
				try:
					result = ydl.extract_info(url, download=True)
					self.sendEmailWithDownload.delay(self.getLocalDownloadPath(result['id']), self.userEmail, self.sender)
				except Exception as e:
					print "Can't download audio! %s\n" % traceback.format_exc()
					raise DownloadError('Download not permitted')
		return result

	@abstractmethod
	def getSongData(self, url):
		"""Get song metadata"""
		return

	def getLocalDownloadPath(self, id):
		if not os.path.exists(self.localDownloadsDirectory):
			os.makedirs(self.localDownloadsDirectory)

		filename = (".").join((id, 'mp3'))
		fullDownloadPath = ("/").join((self.localDownloadsDirectory, filename))

		return fullDownloadPath


	@celery.task(bind=True)
	def sendEmailWithDownload(self, url, userEmail, sender):
		recipients = [userEmail]
		subject = 'Your HrtBeat download'
		messageObject = Message(subject, sender=sender, recipients=recipients)
		messageObject.body = 'Here is your download ' + url
		with app.app_context():
			mail.send(messageObject)

class YoutubeProvider(BaseMediaProvider):
	def getSongData(self, url):
		return

class SoundCloudProvider(BaseMediaProvider):
	def getSongData(self, url):
		return

class BeatportProvider(BaseMediaProvider):
	def getSongData(self, url):
		return