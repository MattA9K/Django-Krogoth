"""

 * KROGOTH v0.9.53
 * Copyright (C) 2019 Matt Andrzejczuk < matt@jawn.it >

 * KROGOTH can not be copied and/or distributed without the express
 * permission of Matt Andrzejczuk.

 * February, 2019

"""
print('\033[94m\033[1mLoading Krogoth STAGING ENV...\033[0m\033[0m')
import os
import socket
import subprocess

from django.core.mail import *

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '-ic*v=-p%!6#0ki%kj2l&@4e_a_j!7xm7g9wmxu%8f$9xj*2ht'

DEBUG = False
ALLOWED_HOSTS = ['*']



SESSION_REDIS_HOST = ''
SESSION_REDIS_PORT = ''
POSTGRES_ENV_POSTGRES_USER = ''
POSTGRES_ENV_POSTGRES_PASSWORD = ''
POSTGRES_PORT_5432_TCP_ADDR = ''
POSTGRES_PORT_5432_TCP_PORT = ''
try:
    SESSION_REDIS_HOST = os.environ["REDIS_PORT_6379_TCP_ADDR"]
    SESSION_REDIS_PORT = os.environ["REDIS_PORT_6379_TCP_PORT"]
    POSTGRES_ENV_POSTGRES_USER = os.environ["POSTGRES_ENV_POSTGRES_USER"]
    POSTGRES_ENV_POSTGRES_PASSWORD = os.environ["POSTGRES_ENV_POSTGRES_PASSWORD"]
    POSTGRES_PORT_5432_TCP_ADDR = os.environ["POSTGRES_PORT_5432_TCP_ADDR"]
    POSTGRES_PORT_5432_TCP_PORT = os.environ["POSTGRES_PORT_5432_TCP_PORT"]
except:
    SESSION_REDIS_HOST = '172.17.0.3'
    SESSION_REDIS_PORT = '6379'
    POSTGRES_ENV_POSTGRES_USER = 'jawn'
    POSTGRES_ENV_POSTGRES_PASSWORD = 'gFmMlyGgINNd4mUKfJvyIQjmpL0K4572lvqhalkuC4WyZ8vUqCASS'
    POSTGRES_PORT_5432_TCP_ADDR = '172.17.0.2'
    POSTGRES_PORT_5432_TCP_PORT = '5432'

# App will serve frontend from '/static/compiled' rather than slowly generating
# frontend code dynamically. Use True for production.
STATIC_KROGOTH_MODE = True
# RESTART UWSGI TO SEE COMPILED CHANGES:
# docker exec armprime supervisorctl restart app-uwsgi

# Application definition
REST_FRAMEWORK = {
    'PAGE_SIZE': 100,
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.AllowAny',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        # 'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.TokenAuthentication',
        # 'rest_framework.authentication.SessionAuthentication',
    ),
    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend']
    # 'DEFAULT_THROTTLE_CLASSES': (
    #     'rest_framework.throttling.ScopedRateThrottle',
    #     'rest_framework.throttling.AnonRateThrottle',
    #     'rest_framework.throttling.UserRateThrottle'
    # ),
    # 'DEFAULT_THROTTLE_RATES': {
    #     'anon': '28100/day',
    #     'user': '20010/day'
    # }
}
AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
)
INSTALLED_APPS = (
    # 'suit',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.facebook',
    'allauth.socialaccount.providers.instagram',
    'allauth.socialaccount.providers.twitter',

    'polymorphic',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # 'django.contrib.postgres',

    'django.contrib.sites',
    'django_filters',
    'django_extensions',
    'ws4redis',
    'rest_framework_docs',
    'rest_framework',
    'rest_framework.authtoken',

    # 'allauth.socialaccount',
    # 'rest_framework_swagger',
    # 'krogoth_3rdparty_api',
    'krogoth_gantry',
    'rest_auth',
)

MIDDLEWARE = [
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
]

ROOT_URLCONF = 'jawn.urls'
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'ws4redis.context_processors.default',
            ],
        },
    },
]
# USE WITH DOCKER ONLY:
WSGI_APPLICATION = 'jawn.wsgi.application'
# USE WITHOUT DOCKER:
# WSGI_APPLICATION = 'jawn.wsgi_no_docker.application'

db_name = 'jawn'
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql_psycopg2',
#         'NAME': db_name,
#         'USER': POSTGRES_ENV_POSTGRES_USER,
#         'PASSWORD': POSTGRES_ENV_POSTGRES_PASSWORD,
#         'HOST': POSTGRES_PORT_5432_TCP_ADDR,
#         'PORT': POSTGRES_PORT_5432_TCP_PORT,
#     }
# }
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR + '/db.sqlite3',
    }
}

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True
STATIC_URL = '/static/' # static files
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)
STATIC_ROOT = ('/usr/src/volatile/static/')
MEDIA_ROOT = '/usr/src/volatile/media/' # user uploads root path
MEDIA_URL = '/media/'
SITE_ID = 2
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
REST_AUTH_SERIALIZERS = {
    'USER_DETAILS_SERIALIZER': 'krogoth_gantry.functions.serializers_chat.GetUserSerializer',
}
APPEND_SLASH = True


# <WebSocket Config>
#    - WebSocket messages are stored in a Redis DB, not in PostgreSQL DB.
# CACHES = {
#     "default": {
#         "BACKEND": "django_redis.cache.RedisCache",
#         "LOCATION": "redis://" + SESSION_REDIS_HOST + ":" + SESSION_REDIS_PORT + "/0",
#         "OPTIONS": {
#             "CLIENT_CLASS": "django_redis.client.DefaultClient",
#             "SERIALIZER": "django_redis.serializers.json.JSONSerializer",
#         }
#     }
# }
WEBSOCKET_URL = '/ws/'
# JavaScript mode will assume user access token is not in header of socket connection.
JAVASCRIPT_MODE = True
WS4REDIS_EXPIRE = 2
WS4REDIS_HEARTBEAT = '--heartbeat--'
WS4REDIS_PREFIX = 'demo'

### DEFAULTS:
# WS4REDIS_CONNECTION = getattr(settings, 'WS4REDIS_CONNECTION', {
#     'host': 'localhost',
#     'port': 6379,
#     'db': 0,
#     'password': None,
# })
SESSION_ENGINE = 'redis_sessions.session'
SESSION_REDIS_PREFIX = 'session'
# </WebSocket Config>

WS4REDIS_CONNECTION = {
    'host': SESSION_REDIS_HOST,
    'port': SESSION_REDIS_PORT,
    'db': 0,
    'password': None,
}

KROGOTH_TRACE = True
import sys
import django
import rest_framework
try:
    print('\033[35mPython %s\033[0m' % (str(sys.version)[0:6]))
    print('\033[36mInitializing Django \033[1m' +
          str(django.VERSION[0]) + '.' + str(django.VERSION[1]) + '.' + str(django.VERSION[2]) + '\033[0m\033[0m')
    print('\033[94mDjango REST Framework \033[1m' + str(rest_framework.VERSION) + '\033[0m\033[0m')
    bash_cmd = ['git', 'rev-list', '--count', 'HEAD']
    get_build_cmd = str(subprocess.check_output(bash_cmd))
    current_build_1 = ''
    current_build_2 = ''
    v1 = ''
    v2 = ''
    v3 = ''
    total_commits = int(subprocess.check_output(bash_cmd).decode('utf-8').removesuffix('\n'))
    if total_commits >= 1000:
        as_str = str(total_commits)
        v1 = as_str[:1]
        v2 = as_str[1:2]
        v3 = as_str[2:]
    else:
        as_str = str(total_commits)
        v3 = as_str[1:]
        v2 = as_str[:1]
        v1 = '0'
    if v3 == '00':
        v3 = '0'
    else:
        rm_0s = v3.replace('10', '1').replace('20', '2').replace('30', '3').replace('40', '4')
        v3 = rm_0s.replace('50', '5').replace('60', '6').replace('70', '7').replace('80', '8').replace(
            '90', '9')
    APP_VERSION = v1 + '.' + v2 + '.' + v3
    print('\033[1m\033[92mKrogoth ' + APP_VERSION + ' \033[0m\033[0m')
    print()
except:
    print('\033[31mDjango initialized, but the version is unknown...\033[0m')
