# Django settings for djopenid project.

import os
import sys
import warnings
from os.path import join,  dirname,  normpath

try:
    import openid
except ImportError, e:
    warnings.warn("Could not import OpenID library.  Please consult the djopenid README.")
    sys.exit(1)

PROJECT_ROOT = join(dirname(normpath(__file__)), '..')
DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@domain.com'),
)

MANAGERS = ADMINS

DATABASE_ENGINE = 'sqlite3'           # 'postgresql', 'mysql', 'sqlite3' or 'ado_mssql'.
DATABASE_NAME = '/tmp/test.db'             # Or path to database file if using sqlite3.
DATABASE_USER = ''             # Not used with sqlite3.
DATABASE_PASSWORD = ''         # Not used with sqlite3.
DATABASE_HOST = ''             # Set to empty string for localhost. Not used with sqlite3.
DATABASE_PORT = ''             # Set to empty string for default. Not used with sqlite3.

# Local time zone for this installation. All choices can be found here:
# http://www.postgresql.org/docs/current/static/datetime-keywords.html#DATETIME-TIMEZONE-SET-TABLE
TIME_ZONE = 'America/Chicago'

# Language code for this installation. All choices can be found here:
# http://www.w3.org/TR/REC-html40/struct/dirlang.html#langcodes
# http://blogs.law.harvard.edu/tech/stories/storyReader$15
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

STATIC_ROOT = join(PROJECT_ROOT, 'static')
STATIC_URL = '/static/'
MEDIA_ROOT = join(PROJECT_ROOT,  'media')
MEDIA_URL = '/media/'
STATIC_LOCAL_ROOT = join(PROJECT_ROOT, 'static_local')
STATIC_LOCAL_URL = '/static_local/'


# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/static/admin_media/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'u^bw6lmsa6fah0$^lz-ct$)y7x7#ag92-z+y45-8!(jk0lkavy'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
#     'django.template.loaders.eggs.load_template_source',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.doc.XViewMiddleware',
)

ROOT_URLCONF = 'project.urls'

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth', 
#    'django.core.context_processors.static',,
    'django.core.context_processors.debug', 
    'django.core.context_processors.i18n', 
)

TEMPLATE_DIRS = (
    os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'templates')),
)

INSTALLED_APPS = (
    'django.contrib.admin', 
    'django.contrib.sites',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'south',
    'core',
    'consumer',
    'server',
    'django_ec2',
    'trade',
)

OPENID_URL = 'http://steamcommunity.com/openid'
DB_STORE = 'postgresql'
OPENID_TABLE_PREFIX = 'openid_'