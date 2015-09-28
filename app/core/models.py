from app import db, manager, migrate

class LinkList(db.Model):
	__tablename__ = 'link_list'
	id = db.Column(db.Integer, primary_key=True)
	link_list_access_key = db.Column(db.String(80), unique=True)
	links = db.relationship('Link', backref='LinkList')
	subscribers = db.relationship('Subscriber', backref='LinkList')
	admin_user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


	def __init__(self, link_list_access_key):
		self.link_list_access_key = link_list_access_key

	def getSubscribersDataList(self):
		subscribersLength = len(self.subscribers)
		subscribersDataList = []
		for subscriberObject in self.subscribers:
			subscribersDataList.append(subscriberObject.getSubscriberData())
		return subscribersDataList

	def getLinksDataList(self):
		linksLength = len(self.links)
		linksDataList = []
		for linkObject in self.links:
			linksDataList.append(linkObject.getLinkData())
		return linksDataList

	def getSubscriberCount(self):
		return len(self.subscribers)

class Link(db.Model):
	__tablename__ = 'link'
	id = db.Column(db.Integer, primary_key=True)
	song_artist = db.Column(db.String(100))
	song_title = db.Column(db.String(200))
	song_url = db.Column(db.Text)
	song_provider = db.Column(db.Text)
	click_count = db.Column(db.Integer)
	download_count = db.Column(db.Integer)
	link_list_id = db.Column(db.Integer, db.ForeignKey('link_list.id'))


	def __init__(self, song_artist, song_title, song_url, song_provider, link_list_id):
		self.song_artist = song_artist
		self.song_title = song_title
		self.song_url = song_url
		self.song_provider = song_provider
		self.link_list_id = link_list_id
		self.click_count = 0
		self.download_count = 0

	def getLinkData(self):
		return {'songArtist' : self.song_artist, 'songTitle' : self.song_title, 'songUrl' : self.song_url, 
		'songProvider' : self.song_provider, 'clickCount': self.click_count, 'downloadCount': self.download_count,
		'linkId': self.id, 'linkListId' : self.link_list_id}

class Subscriber(db.Model):
	__tablename__ = 'link_list_subscriber'
	id = db.Column(db.Integer, primary_key=True)
	email = db.Column(db.String(160), unique=True)
	link_list_id = db.Column(db.Integer, db.ForeignKey('link_list.id'))

	def __init__(self, email, link_list_id):
		self.email = email
		self.link_list_id = link_list_id

	def getSubscriberData(self):
		return {'id' : self.id, 'email' : self.email, 'linkListId' : self.link_list_id}