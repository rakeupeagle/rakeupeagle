# Local
# First-Party
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration
from sentry_sdk.integrations.redis import RedisIntegration
from sentry_sdk.integrations.rq import RqIntegration

from .base import *

# Core
SECURE_SSL_REDIRECT = True
ALLOWED_HOSTS = [
    '.rakeupeagle.com',
    '.herokuapp.com',
]

# SendGrid
EMAIL_BACKEND = "sendgrid_backend.SendgridBackend"
SENDGRID_API_KEY = env("SENDGRID_API_KEY")

# Media File Management
CLOUDINARY_STORAGE = {
    'MEDIA_URL': 'rakeupeagle',
}
CLOUDINARY_URL = env("CLOUDINARY_URL")
DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'

# Sentry
sentry_sdk.init(
    dsn=env("SENTRY_DSN"),
    integrations=[
        DjangoIntegration(),
        RqIntegration(),
        RedisIntegration(),
    ],
    send_default_pii=True,
    request_bodies='always',
    release=env("HEROKU_SLUG_COMMIT"),
    traces_sample_rate = .1,
    _experiments = {
        "auto_enabling_integrations":
        True,
    },
)

INSTALLED_APPS += [
    'cloudinary_storage',
    'cloudinary',
]
