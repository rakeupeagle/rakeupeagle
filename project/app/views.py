# Django
# Standard Libary
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
    return render(
        request,
        'app/index.html',
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
