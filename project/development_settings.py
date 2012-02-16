from settings import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'djopenid',
        'USER': 'djopenid',
        'PASSWORD': 'djopenid',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}