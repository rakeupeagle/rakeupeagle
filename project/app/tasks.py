# Standard Libary
import csv

# Third-Party
import geocoder
from django_rq import job

# Django
from django.core.mail import EmailMultiAlternatives
from django.db.models import Sum
from django.template.loader import render_to_string

# Local
from .models import Recipient
from .models import Volunteer


# Utility
def build_email(template, subject, from_email, context=None, to=[], cc=[], bcc=[], attachments=[], html_content=None):
    body = render_to_string(template, context)
    if html_content:
        html_rendered = render_to_string(html_content, context)
    email = EmailMultiAlternatives(
        subject=subject,
        body=body,
        from_email=from_email,
        to=to,
        cc=cc,
        bcc=bcc,
    )
    if html_content:
        email.attach_alternative(html_rendered, "text/html")
    for attachment in attachments:
        with attachment[1].open() as f:
            email.attach(attachment[0], f.read(), attachment[2])
    return email

@job
def send_email(email):
    return email.send()


@job
def geocode_address(address):
    full = f"{address}, Eagle, ID  83616"
    response = geocoder.google(full)
    if not response.ok:
        raise ValueError("{0}".format(address))
    return response.json

# def export_csv():
#     rs = Recipient.objects.annotate(
#         total=Sum('assignments__volunteer__number')
#     ).order_by(
#         'size',
#         'total',
#     )
#     with open('export.csv', 'w') as f:
#         writer = csv.writer(f)
#         writer.writerow([
#             'Name',
#             'Address',
#             'Phone',
#             'Email',
#             'Dog',
#             'Size',
#             'Group(s)',
#             'Total',
#         ])
#         for r in rs:
#             gs = r.assignments.values_list('volunteer__name', 'volunteer__number')
#             groups = "; ".join(["{0} - {1}".format(g[0], g[1]) for g in gs])
#             writer.writerow([
#                 r.name,
#                 r.address,
#                 r.phone,
#                 r.email,
#                 r.is_dog,
#                 r.get_size_display(),
#                 groups,
#                 r.total,
#             ])


@job
def followup_email(recipient):
    email = build_email(
        template='emails/followup.txt',
        subject='Rake Up Eagle Follow-Up Details',
        from_email='Michelle Erekson (Rake Up Eagle) <emerekson@gmail.com>',
        context={'recipient': recipient},
        to=[recipient.email],
        cc=['dbinetti@gmail.com', 'mnwashow@yahoo.com'],
        bcc=['emerekson@gmail.com'],
    )
    return email.send()
