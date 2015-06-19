from app import db

class Helpers():
	@staticmethod
	def deleteObjectFromDb(object):
		db.session.delete(object)
		db.session.commit()
		return True

	@staticmethod
	def addObjectToDb(object):
		db.session.add(object)
		db.session.commit()
		return True

class LinkListHelpers():
	@staticmethod
	def getLinkListIdFromLinkListAccessKey(linkListAccessKey):
		linkList = LinkList.query.filter_by(link_list_access_key=linkListAccessKey).first()
		return linkList.id