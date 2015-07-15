from abc import abstractmethod
import traceback
import os
import youtube_dl
import soundcloud
import beatport

class BaseMediaProvider:
	localDownloadsDirectory = 'downloads'

	@abstractmethod
	def downloadSong(self, url):
		"""Return the file in mp3 format based on the url"""
		return

	@abstractmethod
	def getSongData(self, url):
		"""Get song metadata"""
		return
	"""youtube_dl package can be used for other providers besides just youtube"""
	def getYoutubeDlPath(self, songTitle, songId):
		return '%x-%y.%z' % (songTitle, songId, 'mp3')

	def getLocalDownloadPath(self, artist, title):
		if not os.path.exists(self.localDownloadsDirectory):
			os.makedirs(self.localDownloadsDirectory)

		return os.path.join(self.localDownloadsDirectory, "%s--%s.mp3" % (title, artist))

class YoutubeProvider(BaseMediaProvider):
	def downloadSong(self, url, artist, title):
		ydl_opts = {
			'format': 'bestaudio/best',
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
					os.rename(self.getYoutubeDlPath(result['title'], result['id']), localDownloadPath)
				except Exception as e:
					print "Can't download audio! %s\n" % traceback.format_exc()
		return

	def getSongData(self, url):
		return

class SoundCloudProvider(BaseMediaProvider):
	def downloadSong(self, url):
		return

	def getSongData(self, url):
		return

class BeatportProvider(BaseMediaProvider):
	def downloadSong(self, url):
		return

	def getSongData(self, url):
		return