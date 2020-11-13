# Django
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.shortcuts import render
from django.template.loader import render_to_string

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
    return render(
        request,
        'app/handout.html',
        context={
            'volunteer': volunteer,
        }
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
