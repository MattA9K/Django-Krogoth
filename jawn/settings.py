import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '-ic*v=-p%!6#0ki%kj2l&@4e_a_j!7xm7g9wmxu%8f$9xj*2ht'

DEBUG = True
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
    print("")
    SESSION_REDIS_HOST = '127.0.0.1'
    SESSION_REDIS_PORT = '7070'
    POSTGRES_ENV_POSTGRES_USER = 'jawn'
    POSTGRES_ENV_POSTGRES_PASSWORD = 'xzxzf87d93a3f325574900aa2f5626e3844a903ffb64bed152ae124d2e79xzxz'
    POSTGRES_PORT_5432_TCP_ADDR = '172.17.0.3'
    POSTGRES_PORT_5432_TCP_PORT = '5432'

# App will serve frontend from '/static/compiled' rather than slowly generating
# frontend code dynamically. Use True for production.
STATIC_KROGOTH_MODE = False

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

 # ---- ----- ---- ----- ----- ---- ---- ---- ----- ---- ---- ----     NO-DOCKER MODE. SQLIGHT ONLY
    # 'django.contrib.postgres',
# ---- ----- ---- ----- ----- ---- ---- ---- ----- ---- ---- ----      POSTGRES NOT ACTIVE. PROBABLY DEVELOPMENT MODE PYCHARM

    'django.contrib.sites',
    'django_filters',
    'django_extensions',
    'ws4redis',
    'rest_framework_docs',
    'rest_framework',
    'rest_framework.authtoken',

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
    'allauth.account.middleware.AccountMiddleware',
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




WSGI_APPLICATION = 'jawn.wsgi.application' # USE WITH DOCKER ONLY
# WSGI_APPLICATION = 'jawn.wsgi_no_docker.application' # USE WITHOUT DOCKER

db_name = 'jawn'
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': db_name,
        'USER': POSTGRES_ENV_POSTGRES_USER,
        'PASSWORD': POSTGRES_ENV_POSTGRES_PASSWORD,
        'HOST': POSTGRES_PORT_5432_TCP_ADDR,
        'PORT': POSTGRES_PORT_5432_TCP_PORT,
    }
}
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR + '/db.sqlite3',
#     }
# }



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
MEDIA_ROOT = '/usr/src/app/media/'  # user uploads root path
MEDIA_URL = '/media/'
SITE_ID = 2
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
REST_AUTH_SERIALIZERS = {
    'USER_DETAILS_SERIALIZER': 'krogoth_gantry.functions.serializers_chat.GetUserSerializer',
}
APPEND_SLASH = True

# - - - - - - <WebSocket Config> - - - - - -
CACHES = {
    # "default": {
    #     "BACKEND": "django_redis.cache.RedisCache",
    #     "LOCATION": "redis://" + SESSION_REDIS_HOST + ":" + SESSION_REDIS_PORT + "/0",
    #     "OPTIONS": {
    #         "CLIENT_CLASS": "django_redis.client.DefaultClient",
    #         "SERIALIZER": "django_redis.serializers.json.JSONSerializer",
    #     }
    # }
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'default-locmemcache',
        'TIMEOUT': 5,  # seconds
    }
}
WEBSOCKET_URL = '/ws/'
# JavaScript mode will assume user access token is not in header of socket connection.
JAVASCRIPT_MODE = True
WS4REDIS_EXPIRE = 2
WS4REDIS_HEARTBEAT = '--heartbeat--'
WS4REDIS_PREFIX = 'demo'

SESSION_ENGINE = 'redis_sessions.session'
SESSION_REDIS_PREFIX = 'session'
# - - - - - - </WebSocket Config> - - - - - -


WS4REDIS_CONNECTION = {
    'host': SESSION_REDIS_HOST,
    'port': SESSION_REDIS_PORT,
    'db': 0,
    'password': None,
}

KROGOTH_TRACE = True
