# Django
# Standard Libary
import csv
from urllib.parse import urlencode

from django.conf import settings
from django.contrib import messages
from django.core.files.base import ContentFile
from django.http import FileResponse
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.shortcuts import render
from django.template.loader import render_to_string

# First-Party
import pydf

# Local
from .forms import RecipientForm
from .models import Volunteer
from .tasks import build_email
from .tasks import send_email


# Root
def index(request):
    pictures = ["app/{0}.jpeg".format(x) for x in range(1, 56)]
    return render(
        request,
        'app/index.html',
        context={
            'pictures': pictures,
        }
    )

def recipients(request):
    form = RecipientForm(
        request.POST or None,
    )
    if form.is_valid():
        recipient=form.save()
        messages.success(
            request,
            "Submitted!",
        )
        email = build_email(
            template='emails/confirmed.txt',
            subject='Rake Up Eagle Confirmation',
            context={'recipient': recipient},
            to=[recipient.email],
            from_email='Eagle Middle School PTO <eaglemiddlepto@gmail.com>',
            bcc=['dbinetti@gmail.com', 'mnwashow@yahoo.com'],
        )
        send_email.delay(email)
        return redirect('confirmation')
    return render(
        request,
        'app/recipients.html',
        context={
            'form': form,
        }
    )

def handouts(request):
    volunteers = Volunteer.objects.order_by('name')
    return render(
        request,
        'app/handouts.html',
        context={
            'volunteers': volunteers,
        }
    )


def handout(request, volunteer_id):
    volunteer = get_object_or_404(Volunteer, pk=volunteer_id)
    url = 'https://maps.googleapis.com/maps/api/staticmap?markers={0},{1}&zoom=13&size=300x150&scale=1&key={2}'.format(
        volunteer.recipient.geo['lat'],
        volunteer.recipient.geo['lng'],
        settings.GOOGLE_API_KEY,
    )
    return render(
        request,
        'app/handout.html',
        context={
            'volunteer': volunteer,
            'recipient': volunteer.recipient,
            'mapurl': url,
        }
    )

def handout_pdf(request, volunteer_id):
    volunteer = get_object_or_404(Volunteer, pk=volunteer_id)
    context={
        'volunteer': volunteer,
        'recipient': volunteer.recipient,
        'map': map,
    }
    rendered = render_to_string('app/handout.html', context)
    pdf = pydf.generate_pdf(
        rendered,
        enable_smart_shrinking=False,
        orientation='Portrait',
        margin_top='10mm',
        margin_bottom='10mm',
    )
    content = ContentFile(pdf)
    return FileResponse(
        content,
        as_attachment=True,
        filename='rake_up_eagle_handout.pdf',
    )


def handout_pdfs(request):
    volunteers = Volunteer.objects.order_by('name')
    output = ''
    for volunteer in volunteers:
        context={
            'volunteer': volunteer,
            'recipient': volunteer.recipient,
            'map': map,
        }
        rendered = render_to_string('app/handout.html', context)
        output += "<br>"+rendered
    pdf = pydf.generate_pdf(
        output,
        enable_smart_shrinking=False,
        orientation='Portrait',
        margin_top='10mm',
        margin_bottom='10mm',
    )
    content = ContentFile(pdf)
    return FileResponse(
        content,
        as_attachment=True,
        filename='handouts.pdf',
    )



def export_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="export.csv"'
    vs = Volunteer.objects.order_by('name')

    writer = csv.writer(response)
    writer.writerow([
        'Volunteer',
        'Phone',
        'Number',
        'Recipient',
        'Address',
        'Phone',
        'Email',
        'Dog',
        'Size',
    ])
    for v in vs:
        writer.writerow([
            v.name,
            v.phone,
            v.number,
            v.recipient.name,
            v.recipient.address,
            v.recipient.phone,
            v.recipient.email,
            v.recipient.is_dog,
            v.recipient.get_size_display(),
        ])
    return response



def confirmation(request):
    return render(
        request,
        'app/confirmation.html',
    )

def robots(request):
    rendered = render_to_string(
        'robots.txt',
    )
    return HttpResponse(
        rendered,
        content_type="text/plain",
    )

def sitemap(request):
    rendered = render_to_string(
        'sitemap.txt',
    )
    return HttpResponse(
        rendered,
        content_type="text/plain",
    )
