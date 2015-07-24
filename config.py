# Statement for enabling the development environment
DEBUG = True

# Define the application directory
import os
BASE_DIR = os.path.abspath(os.path.dirname(__file__))  

# Define the database configuration
SQLALCHEMY_DATABASE_URI = 'mysql://root:root@localhost:3306/HrtBeat'
DATABASE_CONNECT_OPTIONS = {}

THREADS_PER_PAGE = 2

# Enable protection against Cross-site Request Forgery (CSRF)
CSRF_ENABLED = False
WTF_CSRF_ENABLED = False

# Secret key for signing session data
CSRF_SESSION_KEY = 'secret'

# Secret key for signing cookies
SECRET_KEY = 'secret'

#Flask-Security parameters
SECURITY_PASSWORD_HASH = 'pbkdf2_sha512'
SECURITY_TRACKABLE = True
SECURITY_PASSWORD_SALT = 'sulochana'
SECURITY_LOGIN_URL = '/auth/login'
SECURITY_LOGIN_USER_TEMPLATE = 'select.html'


