from pathlib import Path

import my_settings

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = my_settings.SECRET_KEY

DEBUG = True

ALLOWED_HOSTS = ['*']



INSTALLED_APPS = [
    # 'django.contrib.admin',
    # 'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corsheaders',
    'user',
    'property',
    'reservation',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    # 'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
]

ROOT_URLCONF = 'airbitnbyte.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'airbitnbyte.wsgi.application'

DATABASES = my_settings.DATABASES

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATIC_URL = '/static/'

APPEND_SLASH = False

##CORS
CORS_ORIGIN_ALLOW_ALL= True
CORS_ALLOW_CREDENTIALS = True

#CORS_ORIGIN_WHITELIST = (
#       'http://localhost:3000',    #React 도메인
#       'http://localhost:8000',    #Django 도메인
#)

CORS_ALLOW_METHODS = (
    'DELETE',
    'GET',
    'OPTIONS',
    'PATCH',
    'POST',
    'PUT',
)

CORS_ALLOW_HEADERS = (
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
    'client',
    'token',
)

#LOGGING = {
#    'disable_existing_loggers': False,
#    'version': 1,
#    'formatters': {
#         'verbose': {
#            'format': '{asctime} {levelname} {message}',
#            'style': '{'
#        },
#    },
#    'handlers': {
#        'console': {
#            'class'     : 'logging.StreamHandler',
#            'formatter' : 'verbose',
#            'level'     : 'DEBUG',
#        },
#        'file': {
#            'level'     : 'DEBUG',
#            'class'     : 'logging.FileHandler',
#            'formatter' : 'verbose',
#            'filename'  : 'debug.log',
#        },
#    },
#    'loggers': {
#        'django.db.backends': {
#            'handlers' : ['console','file'],
#            'level'    : 'DEBUG',
#            'propagate': False,
#        },
#    },
#}
