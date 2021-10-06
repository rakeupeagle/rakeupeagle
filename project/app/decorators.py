# -*- coding: utf-8 -*-

"""
Useful decorators.
"""

from functools import wraps

from django.conf import settings
from django.http import HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from twilio.request_validator import RequestValidator


def twilio(f):
    """
    This decorator provides several helpful shortcuts for writing Twilio views.

        - It ensures that only requests from Twilio are passed through. This
          helps protect you from forged requests.

        - It ensures your view is exempt from CSRF checks via Django's
          @csrf_exempt decorator. This is necessary for any view that accepts
          POST requests from outside the local domain (eg: Twilio's servers).

        - It enforces the blacklist. If you've got any ``Caller``s who are
          blacklisted, any requests from them will be rejected.

        - It allows your view to (optionally) return TwiML to pass back to
          Twilio's servers instead of building an ``HttpResponse`` object
          manually.

        - It allows your view to (optionally) return any ``twilio.Verb`` object
          instead of building a ``HttpResponse`` object manually.

          .. note::
            The forgery protection checks ONLY happen if ``settings.DEBUG =
            False`` (aka, your site is in production).

    Usage::

        from twilio import twiml

        @twilio_view
        def my_view(request):
            r = twiml.Response()
            r.message('Thanks for the SMS message!')
            return r
    """


    @require_POST
    @csrf_exempt
    @wraps(f)
    def decorator(request, *args, **kwargs):
        # When using `method_decorator` on class methods,
        # I haven't been able to get any class views.
        # i would like more research before just taking the check out.

        # Forgery check
        try:
            validator = RequestValidator(settings.TWILIO_AUTH_TOKEN)
            url = request.build_absolute_uri()
            signature = request.META['HTTP_X_TWILIO_SIGNATURE']
        except (AttributeError, KeyError):
            return HttpResponseForbidden()

        if not validator.validate(url, request.POST, signature):
            return HttpResponseForbidden()

        # Blacklist check, by default is true
        # check_blacklist = getattr(
        #     settings,
        #     'DJANGO_TWILIO_BLACKLIST_CHECK',
        #     True
        # )
        # if check_blacklist:
        #     blacklisted_resp = get_blacklisted_response(request)
        #     if blacklisted_resp:
        #         return blacklisted_resp

        response = f(request, *args, **kwargs)
        return response
    return decorator
