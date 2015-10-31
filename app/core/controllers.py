from flask import Blueprint, request, render_template, jsonify, json, session
from app.core.models import Link, LinkList, Subscriber
from app.auth.models import User
from app.core.helpers import Helpers, LinkListHelpers
from app import db

core = Blueprint('core', __name__, url_prefix='/core')
@core.route("/")
@core.route("/<email>")
def getApp(email=None):
	if email:
		userData = json.loads(session[email])
		return render_template('app.html', isUserLoggedIn='true', userData = userData)
	else:
		return render_template('app.html')

@core.route("/retrieve/link-list", methods=['POST'])
def getLinkList():
	data = request.get_json()
	linkList = LinkList.query.filter_by(link_list_access_key=data["linkListAccessKey"]).first()
	if not linkList:
		return jsonify(status=False)
	else:
		return jsonify(status=True, id=linkList.id, linkListAccessKey=linkList.link_list_access_key, subscribers=linkList.getSubscribersDataList(), subscriberCount=linkList.getSubscriberCount(), links=linkList.getLinksDataList())

@core.route("/retrieve/user/link-lists", methods=['POST'])
def getLinkListsByUser():
	data = request.get_json()
	adminUserId = data["id"]
	linkLists = LinkListHelpers.getSerializedLinkListsFromAdminUserId(adminUserId)
	return jsonify(linkLists=linkLists, status=True)

@core.route("/create/link-list", methods=['POST'])
def addLinkList():
	data = request.get_json()
	newLinkList = LinkList(link_list_access_key = data["linkListAccessKey"], admin_user_id = data["adminUserId"])
	Helpers.addObjectToDb(newLinkList)
	return jsonify(status=True)

@core.route("/delete/link-list", methods=['POST'])
def deleteLinkList():
	data = request.get_json()
	linkList = LinkList.query.filter_by(link_list_access_key=data["linkListAccessKey"]).first()
	Helpers.deleteObjectFromDb(linkList)
	return jsonify(status=True)

@core.route("/create/subscriber", methods=['POST'])
def addSubscriber():
	data = request.get_json()
	linkListId = LinkListHelpers.getLinkListIdFromLinkListAccessKey(data["linkListAccessKey"])
	newSubscriber = Subscriber(email = data["email"], link_list_id=linkListId)
	Helpers.addObjectToDb(newSubscriber)
	return jsonify(status=True)

@core.route("/retrieve/subscribers", methods="POST")
def getSubscribers():
	data = request.get_json()
	linkListId = LinkListHelpers.getLinkListIdFromLinkListAccessKey()
	subscribers = LinkList.query.filter_by(link_list_access_key=data["linkListAccessKey"]);
	return jsonify(status=True)

@core.route("/delete/subscriber", methods=['POST'])
def deleteSubscriber():
	data = request.get_json()
	subscriber = Subscriber.query.filter_by(id=data["id"]).first()
	Helpers.deleteObjectFromDb(subscriber)
	return jsonify(status=True)

@core.route("/create/link", methods=['POST'])
def addLink():
	data = request.get_json()
	linkListId = LinkListHelpers.getLinkListIdFromLinkListAccessKey(data["linkListAccessKey"])
	newLink = Link(song_artist=data["songArtist"], song_title=data["songTitle"], song_url=data["songUrl"], song_provider=data["songProvider"], link_list_id=linkListId)
	Helpers.addObjectToDb(newLink)
	return jsonify(status=True)

@core.route("/update/link", methods=['POST'])
def updateLink():
	data = request.get_json()
	link = Link.query.filter_by(id=data["id"]).first()
	link.song_artist = data["songArtist"]
	link.song_title = data["songTitle"]
	link.song_url = data["songUrl"]
	link.click_count = data["clickCount"]
	link.download_count = data["downloadCount"]
	db.session.commit()
	return jsonify(status=True)

@core.route("/delete/link", methods=['POST'])
def deleteLink():
	data = request.get_json()
	link = Link.query.filter_by(id=data["id"]).first()
	Helpers.deleteObjectFromDb(link)
	return jsonify(status=True)