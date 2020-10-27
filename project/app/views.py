# Standard Libary
import json
import logging

# Django
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.shortcuts import render
from django.template.loader import render_to_string

# Local
from .forms import RecipientForm
from .models import Recipient
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
        form.save()
        messages.success(
            request,
            "Submitted!",
        )
        email = build_email(
            template='emails/confirmed.txt',
            subject='Rake Up Eagle Confirmation',
            context={'recipient': form.cleaned_data},
            to=[form.cleaned_data['email']],
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


# @login_required
# def volunteer(request, volunteer_id):
#     volunteer = get_object_or_404(Volunteer, id=volunteer_id)
#     if volunteer.id != request.user.volunteer.id:
#         return HttpResponse(status=400)
#     form = VolunteerForm(
#         request.POST or None,
#         instance=volunteer,
#     )
#     if form.is_valid():
#         form.save()
#         messages.success(
#             request,
#             "Saved!",
#         )
#         return redirect('dashboard')
#     return render(
#         request,
#         'app/volunteer.html',
#         context={
#             'form': form,
#         }
#     )
