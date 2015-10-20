from abc import abstractmethod
from app import celery, mail
import traceback
import os
import youtube_dl

class BaseMediaProvider:
	localDownloadsDirectory = 'downloads'

	def __init__(self, user_email):
		self.user_email = user_email


	def sendEmailWithDownload(self):
		return

	def downloadSong(self, url, artist, title):
		ydl_opts = {
			'format': 'bestaudio/best',
			'outtmpl': 'downloads/%(id)s.%(ext)s',
			'postprocessors': [{
				'key': 'FFmpegExtractAudio',
				'preferredcodec': 'mp3',
				'preferredquality': '192'
			}]
		}

		with youtube_dl.YoutubeDL(ydl_opts) as ydl:
			localDownloadPath = self.getLocalDownloadPath(artist, title)
			try:
				os.stat(localDownloadPath)
				print "%s already downloaded, continuing..." % localDownloadPath
			except OSError:
				try:
					result = ydl.extract_info(url, download=True)
				except Exception as e:
					print "Can't download audio! %s\n" % traceback.format_exc()
		return

	@abstractmethod
	def getSongData(self, url):
		"""Get song metadata"""
		return

	def getLocalDownloadPath(self, artist, title):
		if not os.path.exists(self.localDownloadsDirectory):
			os.makedirs(self.localDownloadsDirectory)

		return os.path.join(self.localDownloadsDirectory, "%s--%s.mp3" % (title, artist))

class YoutubeProvider(BaseMediaProvider):
	def getSongData(self, url):
		return

class SoundCloudProvider(BaseMediaProvider):
	def getSongData(self, url):
		return

class BeatportProvider(BaseMediaProvider):
	def getSongData(self, url):
		return