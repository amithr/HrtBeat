import youtube_dl
import 

class BaseProvider:
	@abstractmethod
	def downloadSong(self, url):
		"""Return the file in mp3 format based on the url"""
		return

	@abstractmethod
	def getSongData(self, url):
		"""Get song metadata"""
		return

class YoutubeProvider(BaseProvider):
	def downloadSong(self, url):
		return

	def getSongData(self, url):
		return

class SoundCloudProvider(BaseProvider):
	def downloadSong(self, url):
		return

	def getSongData(self, url):
		return