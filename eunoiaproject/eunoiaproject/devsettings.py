from .settings import *

DEBUG = True
HOST_NAME = 'http://localhost:8080/'

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'postgres',
        'USER': 'postgres',
        'PASSWORD': 'postgres',
        'HOST': 'localhost',
        'PORT': '',
    }
}

# You don't need to set this mandatorily for dev
# You can use the URL in the console for user registration activation


# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'    
EMAIL_USE_SSL = True
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'your smtp server'
EMAIL_HOST_USER = 'username'
EMAIL_HOST_PASSWORD = 'password'
EMAIL_PORT = 123 # PORT



