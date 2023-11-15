from .base import *

# Core
SECURE_SSL_REDIRECT = True
ALLOWED_HOSTS = [
    '.rakeupeagle.com',
    '.herokuapp.com',
]

# Sentry
SENTRY_RELEASE = env("HEROKU_SLUG_COMMIT")

# Sentry
SENTRY_CONFIG['release'] = env("HEROKU_SLUG_COMMIT")
