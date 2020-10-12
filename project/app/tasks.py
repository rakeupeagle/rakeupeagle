
# # Third-Party
# import geocoder
# from auth0.v3.authentication import GetToken
# from auth0.v3.management import Auth0
# from django_rq import job
# from mailchimp3 import MailChimp
# from mailchimp3.helpers import get_subscriber_hash
# from mailchimp3.mailchimpclient import MailChimpError

# # Django
# from django.conf import settings
# from django.core.mail import EmailMultiAlternatives
# from django.template.loader import render_to_string


# def auth0_get_client():
#     get_token = GetToken(settings.AUTH0_DOMAIN)
#     token = get_token.client_credentials(
#         settings.AUTH0_CLIENT_ID,
#         settings.AUTH0_CLIENT_SECRET,
#         'https://{}/api/v2/'.format(settings.AUTH0_DOMAIN),
#     )
#     mgmt_api_token = token['access_token']
#     client = Auth0(
#         settings.AUTH0_DOMAIN,
#         mgmt_api_token,
#     )
#     return client

# @job
# def auth0_delete_user(username):
#     client = auth0_get_client()
#     result = client.users.delete(username)
#     return result


# # Utility
# def build_email(template, subject, context=None, to=[], cc=[], bcc=[], attachments=[], html_content=None):
#     body = render_to_string(template, context)
#     if html_content:
#         html_rendered = render_to_string(html_content, context)
#     email = EmailMultiAlternatives(
#         subject=subject,
#         body=body,
#         from_email='David Binetti <dbinetti@startnormal.com>',
#         to=to,
#         cc=cc,
#         bcc=bcc,
#     )
#     if html_content:
#         email.attach_alternative(html_rendered, "text/html")
#     for attachment in attachments:
#         with attachment[1].open() as f:
#             email.attach(attachment[0], f.read(), attachment[2])
#     return email

# @job
# def send_email(email):
#     return email.send()


# def get_mailchimp_client():
#     enabled = not settings.DEBUG
#     return MailChimp(
#         mc_api=settings.MAILCHIMP_API_KEY,
#         enabled=enabled,
#     )


# @job
# def mailchimp_subscribe_email(email):
#     client = get_mailchimp_client()
#     data = {
#         'email_address': email,
#         'status': 'subscribed',
#     }
#     try:
#         result = client.lists.members.create(
#             list_id=settings.MAILCHIMP_AUDIENCE_ID,
#             data=data,
#         )
#     except MailChimpError as e:
#         result = str(e)
#     return result


# @job
# def mailchimp_delete_email(email):
#     client = get_mailchimp_client()
#     subscriber_hash = get_subscriber_hash(email)
#     client = MailChimp(mc_api=settings.MAILCHIMP_API_KEY)
#     try:
#         result = client.lists.members.delete(
#             list_id=settings.MAILCHIMP_AUDIENCE_ID,
#             subscriber_hash=subscriber_hash,
#         )
#     except Exception as e:
#         return str(e)
#     return result


# @job
# def mailchimp_create_or_update_from_user(user):
#     client = get_mailchimp_client()
#     list_id = settings.MAILCHIMP_AUDIENCE_ID
#     subscriber_hash = get_subscriber_hash(user.email)
#     data = {
#         'status_if_new': 'subscribed',
#         'email_address': user.email,
#         'merge_fields': {
#             'NAME': user.name,
#         }
#     }
#     result = client.lists.members.create_or_update(
#         list_id=list_id,
#         subscriber_hash=subscriber_hash,
#         data=data,
#     )
#     return result


# @job
# def geocode_school(school):
#     full = f"{school.address}, {school.city} {school.state} {school.zipcode}"
#     response = geocoder.google(full)
#     if not response.ok:
#         raise ValueError("{0} - {1}".format(school, response))
#     school.geo = response.json
#     school.lat = response.json['lat']
#     school.lon = response.json['lng']
#     return school.save()
