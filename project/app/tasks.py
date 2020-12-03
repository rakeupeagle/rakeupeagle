# Standard Libary
import csv

# Django
from django.conf import settings
from django.core.files import File
from django.core.files.base import ContentFile
from django.core.mail import EmailMultiAlternatives
from django.db.models import Sum
from django.http import FileResponse
from django.template.loader import render_to_string

# First-Party
from auth0.v3.authentication import GetToken
from auth0.v3.management import Auth0
from django_rq import job

# Local
from .models import Picture
from .models import Recipient


# Auth0
def get_auth0_token():
    get_token = GetToken(settings.AUTH0_DOMAIN)
    token = get_token.client_credentials(
        settings.AUTH0_CLIENT_ID,
        settings.AUTH0_CLIENT_SECRET,
        f'https://{settings.AUTH0_DOMAIN}/api/v2/',
    )
    return token


def get_auth0_client():
    token = get_auth0_token()
    client = Auth0(
        settings.AUTH0_DOMAIN,
        token['access_token'],
    )
    return client

def get_user_data(user_id):
    client = get_auth0_client()
    data = client.users.get(user_id)
    return data

@job
def update_user(user):
    data = get_user_data(user.username)
    user.data = data
    user.name = data.get('name', '')
    user.first_name = data.get('given_name', '')
    user.last_name = data.get('family_name', '')
    user.email = data.get('email', None)
    user.phone = data.get('phone_number', None)
    user.save()
    return user


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


def export_csv():
    rs = Recipient.objects.annotate(
        total=Sum('assignments__volunteer__number')
    ).order_by(
        'size',
        'total',
    )
    with open('export.csv', 'w') as f:
        writer = csv.writer(f)
        writer.writerow([
            'Name',
            'Address',
            'Phone',
            'Email',
            'Dog',
            'Size',
            'Group(s)',
            'Total',
        ])
        for r in rs:
            gs = r.assignments.values_list('volunteer__name', 'volunteer__number')
            groups = "; ".join(["{0} - {1}".format(g[0], g[1]) for g in gs])
            writer.writerow([
                r.name,
                r.address,
                r.phone,
                r.email,
                r.is_dog,
                r.get_size_display(),
                groups,
                r.total,
            ])
        content = ContentFile(f)
        return FileResponse(
            content,
            as_attachment=True,
            filename='export.csv',
        )


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


@job
def post_email(volunteer):
    email = build_email(
        template='emails/post.txt',
        subject='Rake Up Eagle Pictures Posted',
        from_email='Dave Binetti (Rake Up Eagle) <dbinetti@gmail.com>',
        context={'volunteer': volunteer},
        to=[volunteer.email],
        cc=['emerekson@gmail.com', 'mnwashow@yahoo.com'],
        bcc=['dbinetti@gmail.com'],
    )
    return email.send()

@job
def create_and_upload_picture(path):
    with open(path, 'rb') as f:
        imagefile = File(f)
        picture = Picture.objects.create()
        picture.image.save('null', imagefile)
