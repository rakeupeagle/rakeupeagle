import csv

import geocoder
# Django
from django.core.mail import EmailMultiAlternatives
from django.db.models import Sum
from django.template.loader import render_to_string
# First-Party
from django_rq import job

from .models import Assignment
from .models import Recipient
from .models import Volunteer


# Utility
def build_email(template, subject, context=None, to=[], cc=[], bcc=[], attachments=[], html_content=None):
    body = render_to_string(template, context)
    if html_content:
        html_rendered = render_to_string(html_content, context)
    email = EmailMultiAlternatives(
        subject=subject,
        body=body,
        from_email='Eagle Middle School PTO <eaglemiddlepto@gmail.com>',
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

def export_csv():
    rs = Recipient.objects.all()
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
            foo = ["{0} - {1}".format(g[0], g[1]) for g in gs]
            bar = "; ".join(foo)
            total = r.assignments.aggregate(s=Sum('volunteer__number'))['s']
            writer.writerow([
                r.name,
                r.address,
                r.phone,
                r.email,
                r.is_dog,
                r.get_size_display(),
                bar,
                total,
            ])
