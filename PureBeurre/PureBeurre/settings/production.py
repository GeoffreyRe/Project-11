from . import *

ALLOWED_HOSTS = ['134.209.187.239', 'localhost', '127.0.0.1']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ.get("DATABASE_NAME"),
        'USER' : os.environ.get("DATABASE_USER"),
        'PASSWORD' : os.environ.get("DATABASE_PASSWORD"),
        'HOST' : 'LOCALHOST',
        'PORT' : '5432'

    }
}