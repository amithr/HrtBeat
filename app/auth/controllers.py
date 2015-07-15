from flask import Blueprint, request, render_template, jsonify
from app.core.models import Link, LinkList, Subscriber
from app import db

auth = Blueprint('auth', __name__, url_prefix='/auth')

@auth.route('/login')
def login():
	return

@auth.route('/register')
def register():
	return