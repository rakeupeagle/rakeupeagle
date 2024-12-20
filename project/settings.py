import logging.config

from django.contrib.messages import constants as messages
from environ import Env
from environ import Path

# Set Environment
env = Env(
    DEBUG=(bool, False),
    DEFAULT_FROM_EMAIL=(str, 'webmaster@localhost'),
    TIME_ZONE=(str, 'America/Boise'),
    EMAIL_URL=(str, 'smtp://localhost:1025'),
    REDIS_URL=(str, 'redis://localhost:6379/0'),
    RQ_ASYNC=(bool, False),
    ALLOWED_HOSTS=(list, []),
    HEROKU_SLUG_COMMIT=(str, 'Init'),
)

root = Path(__file__) - 2

# Common
DEBUG = env("DEBUG")
BASE_DIR = root()
SECRET_KEY = env("SECRET_KEY")
ROOT_URLCONF = 'urls'
WSGI_APPLICATION = 'wsgi.application'
DEFAULT_AUTO_FIELD = 'hashid_field.HashidAutoField'
ADMINS = [
    ('admin', env("DEFAULT_FROM_EMAIL")),
]
ALLOWED_HOSTS = env.list("ALLOWED_HOSTS")
SESSION_COOKIE_SECURE = not env("DEBUG")
SECURE_SSL_REDIRECT = not env("DEBUG")
CSRF_COOKIE_SECURE = not env("DEBUG")

# Datetime
USE_TZ = True
DATE_FORMAT = 'Y-m-d'
TIME_FORMAT = 'H:i:s'
DATETIME_FORMAT = 'Y-m-d H:i:s'
TIME_ZONE = env("TIME_ZONE")

# HashIDs
HASHID_FIELD_SALT = env("SECRET_KEY")
HASHID_FIELD_MIN_LENGTH = 8
HASHID_FIELD_ENABLE_HASHID_OBJECT = False

# Authentication
AUTH_USER_MODEL = 'app.User'
AUTHENTICATION_BACKENDS = [
    'app.backends.AppBackend',
]
LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'index'
LOGOUT_REDIRECT_URL = 'index'

# Database
DATABASES = {
    'default': env.db()
}
DATABASES['default']['ENGINE'] = 'django.contrib.gis.db.backends.postgis'

# Cache
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.redis.RedisCache",
        "LOCATION": env("REDIS_URL"),
        "OPTIONS": {
                "ssl_cert_reqs": None
        }
    },
}

# RQ
RQ_QUEUES = {
    'default': {
        'URL': env("REDIS_URL"),
        'ASYNC': env("RQ_ASYNC"),
        "SSL": True,
        'SSL_CERT_REQS': None,
    },
}
RQ_SHOW_ADMIN_LINK = True

# Sessions
SESSION_ENGINE = "django.contrib.sessions.backends.cache"
SESSION_CACHE_ALIAS = "default"

# Email
DEFAULT_FROM_EMAIL = env("DEFAULT_FROM_EMAIL")
EMAIL_CONFIG = env.email_url('EMAIL_URL')
vars().update(EMAIL_CONFIG)

# Storage
STATIC_ROOT = root('staticfiles')
STATIC_URL = 'static/'
MEDIA_ROOT = root('mediafiles')
MEDIA_URL = 'media/'
STORAGES = {
    "default": {
        "BACKEND": env("STORAGE_BACKEND"),
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedStaticFilesStorage",
    },
}

# AWS Settings
AWS_ACCESS_KEY_ID = env("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = env("AWS_SECRET_ACCESS_KEY")
AWS_STORAGE_BUCKET_NAME = 'rakeupeagle'
AWS_QUERYSTRING_AUTH = False
AWS_S3_REGION_NAME = 'us-west-2'
AWS_S3_FILE_OVERWRITE = True

# Google
GOOGLE_API_KEY = env("GOOGLE_API_KEY")

# Twilio
TWILIO_ACCOUNT_SID = env("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = env("TWILIO_AUTH_TOKEN")
TWILIO_NUMBER = env("TWILIO_NUMBER")
TWILIO_VERIFY_SID = env("TWILIO_VERIFY_SID")
TWILIO_MESSAGING_SERVICE_SID = env("TWILIO_MESSAGING_SERVICE_SID")

# Phone Numbers
PHONENUMBER_DB_FORMAT = 'NATIONAL'
PHONENUMBER_DEFAULT_REGION = 'US'

# Sentry
SENTRY_CONFIG = {
    'dsn': env("SENTRY_DSN"),
    'environment': env("SENTRY_ENVIRONMENT"),
    'release': env("HEROKU_SLUG_COMMIT"),
    'send_default_pii': True,
}

# Bootstrap override
MESSAGE_TAGS = {
    messages.ERROR: 'danger',
}

# Middleware
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# Templating
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.template.context_processors.request',
            ],
        },
    },
]

# Logging
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
        },
        "rq_console": {
            "level": "INFO",
            "class": "rq.logutils.ColorizingStreamHandler",
        },
    },
    "loggers": {
        "app": {
            "handlers": ["console"],
            "level": "INFO",
        },
        "rq.worker": {
            "handlers": ["rq_console"],
            "level": "INFO"
        },
    },
}


INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.humanize',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.gis',
    'django.contrib.staticfiles',
    'django.contrib.postgres',
    'django_rq',
    'django_fsm',
    'fsm_admin',
    'phonenumber_field',
    'app',
]

# Enable development tools
if DEBUG:
    # Debug Toolbar
    INTERNAL_IPS = ["127.0.0.1"]
    INSTALLED_APPS.append("debug_toolbar")
    MIDDLEWARE.insert(0, "debug_toolbar.middleware.DebugToolbarMiddleware")
    MIDDLEWARE.append("querycount.middleware.QueryCountMiddleware")

    # Whitenoise
    INSTALLED_APPS.append("whitenoise.runserver_nostatic")

    # Redis
    del CACHES['default']['OPTIONS']
    del RQ_QUEUES['default']['SSL']
    del RQ_QUEUES['default']['SSL_CERT_REQS']
