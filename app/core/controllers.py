from flask import Blueprint, request, render_template, jsonify
from app.core.models import Link, LinkList, Subscriber
from app.core.helpers import Helpers, LinkListHelpers
from app import db

core = Blueprint('core', __name__, url_prefix='/core')

@core.route("/select/list")
def selectList():
	return render_template('select.html')

@core.route("/<link_list_access_key>")
def renderApp(link_list_access_key):
	return render_template('app.html', linkListAccessKey=link_list_access_key)

@core.route("/retrieve/link-list", methods=['POST'])
def getLinkList():
	data = request.get_json()
	linkList = LinkList.query.filter_by(link_list_access_key=data["linkListAccessKey"]).first()
	return jsonify(id=linkList.id, name=linkList.name, linkListAccessKey=linkList.link_list_access_key, subscribers=linkList.getSubscribersDataList(), links=linkList.getLinksDataList())

@core.route("/create/link-list", methods=['POST'])
def addLinkList():
	data = request.get_json()
	newLinkList = LinkList(name = data["name"], link_list_access_key = data["linkListAccessKey"])
	Helpers.addObjectToDb(linkList)
	return jsonify(status=True)

@core.route("/delete/link-list", methods=['POST'])
def deleteLinkList():
	data = request.get_json()
	linkList = LinkList.query.filter_by(id=data["id"]).first()
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
	linkListId = LinkListHelpers.getLinkListIdFromLinkListAccessKey
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
	newLink = Link(artist_name=data["artistName"], song_name=data["songName"], song_url=data["songUrl"], song_provider=data["songProvider"], link_list_id=linkListId)
	Helpers.addObjectToDb(newLink)
	return jsonify(status=True)

@core.route("/update/link", methods=['POST'])
def updateLink():
	data = request.get_json()
	link = Link.query.filter_by(id=data["id"]).first()
	link.artist_name = data["artistName"]
	link.song_name = data["songName"]
	link.song_url = data["songUrl"]
	db.session.commit()
	return jsonify(status=True)

@core.route("/delete/link", methods=['POST'])
def deleteLink():
	data = request.get_json()
	link = Link.query.filter_by(id=data["id"]).first()
	Helpers.deleteObjectFromDb(link)
	return jsonify(status=True)