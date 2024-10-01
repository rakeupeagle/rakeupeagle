import logging.config

from django.contrib.messages import constants as messages
from django.utils.log import DEFAULT_LOGGING
from environ import Env
from environ import Path

# Set Environment
env = Env(
    DEBUG=(bool, False),
    DEFAULT_FROM_EMAIL=(str, 'webmaster@localhost'),
    TIME_ZONE=(str, 'America/Boise'),
    EMAIL_URL=(str, 'smtp://localhost:1025'),
    REDIS_URL=(str, 'redis://localhost:6379/0'),
    LOGLEVEL=(str, 'INFO'),
    ACTIVE=(bool, False),
    HEROKU_SLUG_COMMIT=(str, 'Init'),
)

root = Path(__file__) - 2

# Common
BASE_DIR = root()
SECRET_KEY = env("SECRET_KEY")
ROOT_URLCONF = 'urls'
WSGI_APPLICATION = 'wsgi.application'
ADMINS = [
    ('admin', env("DEFAULT_FROM_EMAIL")),
]
USE_L10N = True

# Datetime
USE_TZ = True
DATE_FORMAT = 'Y-m-d'
TIME_FORMAT = 'H:i:s'
DATETIME_FORMAT = 'Y-m-d H:i:s'
TIME_ZONE = env("TIME_ZONE")

# HashIDs
HASHID_FIELD_SALT = env("HASHID_FIELD_SALT")
DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'

# Application Active Flag
ACTIVE = env("ACTIVE")

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

# POSTGIS
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

# Static File Management
STATIC_ROOT = root('staticfiles')
STATIC_URL = '/static/'
STATICFILES_STORAGE = 'whitenoise.storage.StaticFilesStorage'
WHITENOISE_USE_FINDERS = True

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
SENTRY_DSN = env("SENTRY_DSN")
SENTRY_ENVIRONMENT = env("SENTRY_ENVIRONMENT")
SENTRY_CONFIG = {
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
        'DIRS': [
            root('templates'),
        ],
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
LOGGING_CONFIG = None
LOGLEVEL = env("LOGLEVEL")
logging.config.dictConfig({
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'default': {
            'format': '%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
        },
        'django.server': DEFAULT_LOGGING['formatters']['django.server'],
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'default',
        },
        'django.server': DEFAULT_LOGGING['handlers']['django.server'],
    },
    'loggers': {
        # default for all undefined Python modules
        '': {
            'level': 'WARNING',
            'handlers': [
                'console',
            ],
        },
        'app': {
            'level': LOGLEVEL,
            'handlers': [
                'console',
            ],
            'propagate': False,
        },
        # Prevent noisy modules from logging to Sentry
        # 'noisy_module': {
        #     'level': 'ERROR',
        #     'handlers': ['console'],
        #     'propagate': False,
        # },
        # Default runserver request logging
        'django.server': DEFAULT_LOGGING['loggers']['django.server'],
    },
})

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
    'fsm_admin',
    'phonenumber_field',
    'app',
]
