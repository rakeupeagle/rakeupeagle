# Standard Libary
import csv

# Django
from django.core.mail import EmailMultiAlternatives
from django.db.models import Sum
from django.template.loader import render_to_string

# First-Party
from django_rq import job

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
