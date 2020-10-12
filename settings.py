"""
    Global Settings
    ===============

    Global Eve configuration settings
"""

import os, sys
from datetime import datetime

# Make importing sliced up apps easy as pees
sys.path.insert(0, "domain")

# Import the apps - DOMAIN definition (app.DOMAIN)
import domain

__version_info__ = ('0', '9', '8')
APP_VERSION = '.'.join(__version_info__)
APP_AUTHOR = 'Einar Huseby'
APP_LICENSE = 'GPLV1'
APP_COPYRIGHT = '(c) 2014-{} NLF'.format(datetime.now().year)
APP_ALL = ['nlf-backend']

# HATEOAS = False
# OPTIMIZE_PAGINATION_FOR_SPEED = True

AUTH_SESSION_LENGHT = 3600  # Seconds

# @TODO: use sys.argv to parse this as cmdline input
APP_INSTANCES = ['local', 'dev', 'beta', 'prod']
APP_INSTANCE = 'local'  # APP_INSTANCES[0]

if APP_INSTANCE == 'prod':
    MONGO_HOST = 'localhost'
    MONGO_PORT = 27017
    MONGO_USERNAME = ''
    MONGO_PASSWORD = ''
    MONGO_DBNAME = 'nlf-prod'
    # Use default 30s?
    MONGO_CONNECT_TIMEOUT_MS = 200
    APP_HOST = '127.0.0.1'
    APP_PORT = 8080
    APP_INSTANCE_PEM = 'app-public.pem'



elif APP_INSTANCE == 'beta':
    MONGO_HOST = 'localhost'
    MONGO_PORT = 27017
    MONGO_USERNAME = ''
    MONGO_PASSWORD = ''
    MONGO_DBNAME = 'nlf-beta'
    # Use default 30s?
    MONGO_CONNECT_TIMEOUT_MS = 200
    APP_HOST = '127.0.0.1'
    APP_PORT = 8081
    APP_INSTANCE_PEM = 'fnlfbeta-public.pem'

elif APP_INSTANCE in ['dev', 'local']:
    MONGO_HOST = 'localhost'
    MONGO_PORT = 27017
    MONGO_USERNAME = ''
    MONGO_PASSWORD = ''
    MONGO_DBNAME = 'nlf-dev'
    # Use default 30s?
    MONGO_CONNECT_TIMEOUT_MS = 200
    APP_HOST = '127.0.0.1'
    APP_PORT = 8082
    APP_INSTANCE_PEM = 'fnlfbeta-public.pem'

if APP_INSTANCE == 'local':
    E5X_WORKING_DIR = '/home/einar/Development/Luftfartstilsynet/RITS/'
    REQUESTS_VERIFY = False
else:
    E5X_WORKING_DIR = '/www/{}/e5x'.format(APP_INSTANCE)
    # For requests, only local should be false
    REQUESTS_VERIFY = True

# Will also make server watch inode and reload on changes
DEBUG = True

# Our api is located at */api/v1/
URL_PREFIX = 'api'
API_VERSION = 'v1'

# Pagination settings
PAGINATION_LIMIT = 1000000
PAGINATION_DEFAULT = 25

# Enable reads (GET), inserts (POST) and DELETE for resources/collections
# (if you omit this line, the API will default to ['GET'] and provide
# read-only access to the endpoint).
RESOURCE_METHODS = ['GET', 'POST', 'DELETE']

# Enable reads (GET), edits (PATCH) and deletes of individual items
# (defaults to read-only item access). PUT can be enabled to overwrite existing
ITEM_METHODS = ['GET', 'PATCH', 'DELETE', 'PUT']

# We enable standard client cache directives for all resources exposed by the
# API. We can always override these global settings later.
CACHE_CONTROL = 'max-age=20'
CACHE_EXPIRES = 20

# Support json and xml renderer
RENDERERS = ['eve.render.JSONRenderer', 'eve.render.XMLRenderer']

ALLOW_UNKNOWN = False

# ISO
DATE_FORMAT = "%Y-%m-%dT%H:%M:%S.%fZ"

# Will create on PUT when non-existing
# UPSERT_ON_PUT = True

# File storage
EXTENDED_MEDIA_INFO = ['content_type', 'name', 'length']
RETURN_MEDIA_AS_BASE64_STRING = True  # When true loads the file references as base64. Ok for (small) images, rubbish for files (video, documents) and large images Should make a seperate download/streaming resource

# CORS, see http://python-eve.org/config.html#global-configuration:
# X_DOMAINS = ['nlf-az.db02.cloudapp.net','kartverket.no']
# X_HEADERS = None
# X_EXPOSE_HEADERS = None
# X_MAX_AGE = 21600
X_DOMAINS = ['http://localhost:4200', 'https://doc.nlf.no']
X_HEADERS = ['Content-Type', 'If-Match']  # Needed for the "Try it out" buttons
"""
    OP Log
    ======

    The OP Log logs all verbs on nouns

    NB: the collection should for any practical purposes be a capped collection so we don't fill it!!!

"""

OPLOG = False  # Set it to True to enable the Operations Log. Defaults to False.
OPLOG_NAME = 'oplog'  # This is the name of the database collection where the Operations Log is stored. Defaults to oplog.
OPLOG_METHODS = ['DELETE', 'POST', 'PATCH',
                 'PUT']  # List of HTTP methods which operations should be logged in the Operations Log.
OPLOG_ENDPOINT = None  # 'oplog'  # Name of the Operations Log endpoint. If the endpoint is enabled it can be configured like any other API endpoint. Set it to None to disable the endpoint. Defaults to None.
OPLOG_AUDIT = True  # Set it to True to enable the audit feature. When audit is enabled client IP and document changes are also logged to the Operations Log. Defaults to True.
# OPLOG_CUSTOM_FIELDS = {'u': None}

SWAGGER_INFO = {
    'title': 'NLF API',
    'version': APP_VERSION,
    'description': 'RESTful API for the NLF application framework',
    'termsOfService': 'See www.nlf.no',
    'contact': {
        'name': 'Norges Luftsportforbund',
        'email': 'post@nlf.no',
        'url': 'http://www.nlf.no'
    },
    'license': {
        'name': 'GPLV1',
        'url': 'https://github.com/luftsport/nlf-backend/',
    }
}

# LUNGO SPECIFIC
LUNGO = {
    'fallskjerm': {
        'letter': 'f',
        'ors': {
            'send_email_on_create': False
        }
    },
    'motor': {
        'letter': 'g',
        'ors': {
            'send_email_on_create': False
        }
    }
}
# The DOMAIN dict explains which resources will be available and how they will
# be accessible to the API consumer.
DOMAIN = domain.DOMAIN
