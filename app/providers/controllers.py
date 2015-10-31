from flask import Blueprint, request, render_template, jsonify, session
from app import db
from app.providers.helpers import YoutubeProvider, SoundCloudProvider, DownloadError

providers = Blueprint('providers', __name__, url_prefix='/providers')

@providers.route('/download/song', methods=['POST'])
def downloadSong():
	data = request.get_json()
	try:
		YoutubeProvider(data["userEmail"]).downloadSong(data["url"], data["artist"], data["title"])
	except DownloadError as e:
		return jsonify(status=False)
	return jsonify(status=True)

@providers.route('/retrieve/song/data', methods=['POST'])
def retrieveSongData():
	data = request.get_json()
	if data["provider"] == "youtube":
		return
	elif data["provider"] == "soundcloud":
		return
	else:
		return	
	return
