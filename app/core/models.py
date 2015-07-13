from app import db, manager, migrate

class LinkList(db.Model):
	__tablename__ = 'link_list'
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(80), unique=False)
	link_list_access_key = db.Column(db.String(80), unique=True)
	links = db.relationship('Link', backref='LinkList')
	subscribers = db.relationship('Subscriber', backref='LinkList')

	def __init__(self, name, link_list_access_key):
		self.name = name
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

class Link(db.Model):
	__tablename__ = 'link'
	id = db.Column(db.Integer, primary_key=True)
	artist_name = db.Column(db.String(100))
	song_name = db.Column(db.String(200))
	song_url = db.Column(db.Text)
	song_provider = db.Column(db.Text)
	link_list_id = db.Column(db.Integer, db.ForeignKey('link_list.id'))

	def __init__(self, artist_name, song_name, song_url, song_provider, link_list_id):
		self.artist_name = artist_name
		self.song_name = song_name
		self.song_url = song_url
		self.song_provider = song_provider
		self.link_list_id = link_list_id

	def getLinkData(self):
		return {'artistName' : self.artist_name, 'songName' : self.song_name, 'songUrl' : self.song_url, 'songProvider' : self.song_provider, 'linkId': self.id, 'linkListId' : self.link_list_id}

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