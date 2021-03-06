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

#Google API Keys
GOOGLE_CLIENT_ID = '81957407594-cvfrc6gpd35f29nkgmn4lqgb8adlausk.apps.googleusercontent.com'
GOOGLE_CLIENT_SECRET = '5DcaOj-FsdKUUvIrcVNc8SdV'

#Facebook API Keys
FACEBOOK_CLIENT_ID = '1681075138775381'
FACEBOOK_CLIENT_SECRET = '516c9bd0bd9c6196a5befe1aaa39973b'

#Celery Queue Configuration Parameters
CELERY_BROKER_URL = 'redis://localhost:6379/0'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'

#Flask-Mail parameters
MAIL_SERVER = 'smtp.gmail.com'
MAIL_PORT = 465
MAIL_USERNAME = 'amithravindar2493@gmail.com'
MAIL_PASSWORD = 'sulochana2493'
MAIL_USE_TLS = False
MAIL_USE_SSL = True


