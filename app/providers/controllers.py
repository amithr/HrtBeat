from flask import Blueprint, request, render_template, jsonify
from app import db
from app.providers.helpers import YoutubeProvider, SoundCloudProvider

providers = Blueprint('providers', __name__, url_prefix='/providers')

@providers.route('/download/song', methods=['POST'])
def downloadSong():
	data = request.get_json()
	YoutubeProvider().downloadSong(data["url"], data["artist"], data["title"])
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
