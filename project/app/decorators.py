from functools import wraps

from django.conf import settings
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponseForbidden
from twilio.request_validator import RequestValidator


def is_verified(
    view_func=None,
    redirect_field_name=REDIRECT_FIELD_NAME,
    login_url="verify-send"
):
    """
    Decorator for views that checks that the user is verified, redirecting to the login page if necessary.
    """
    actual_decorator = user_passes_test(
        lambda u: u.is_verified,
        login_url=login_url,
        redirect_field_name=redirect_field_name,
    )
    if view_func:
        return actual_decorator(view_func)
    return actual_decorator


def validate_twilio_request(f):
    """Validates that incoming requests genuinely originated from Twilio"""
    @wraps(f)
    def decorated_function(request, *args, **kwargs):
        # Create an instance of the RequestValidator class
        validator = RequestValidator(settings.TWILIO_AUTH_TOKEN)

        # Validate the request using its URL, POST data,
        # and X-TWILIO-SIGNATURE header
        request_valid = validator.validate(
            request.build_absolute_uri(),
            request.POST,
            request.META.get('HTTP_X_TWILIO_SIGNATURE', ''))

        # Continue processing the request if it's valid, return a 403 error if
        # it's not
        if request_valid:
            return f(request, *args, **kwargs)
        return HttpResponseForbidden()
    return decorated_function
