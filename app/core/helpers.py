from app import db
from app.core.models import LinkList

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

	@staticmethod
	def getSerializedLinkListsFromAdminUserId(adminUserId):
		linkLists = LinkList.query.filter_by(admin_user_id = adminUserId).all()
		userLinkListsLength = len(linkLists)
		userLinkLists = []
		for linkListObject in linkLists:
			userLinkLists.append(linkListObject.getLinkListData())
		return userLinkLists