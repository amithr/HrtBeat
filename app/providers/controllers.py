from flask import Blueprint, request, render_template, jsonify
from app import db
from app.providers.helpers import YoutubeProvider, SoundCloudProvider

providers = Blueprint('providers', __name__, url_prefix='/providers')

@providers.route('/download/song')
def downloadSong():
	data = request.get_json()
	if data["provider"] == "youtube":
	elif data["provider"] == "soundcloud"
	else:
		return
	return

@providers.route('/retrieve/song/data')
def retrieveSongData():
	data = request.get_json()
	if data["provider"] == "youtube":
	elif data["provider"] == "soundcloud":
	else:
		return	
	return
