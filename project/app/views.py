# Standard Libary
import csv
import json

# First-Party
import pydf
import requests
# Django
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth import login as log_in
from django.contrib.auth import logout as log_out
from django.contrib.auth.decorators import login_required
from django.core.files.base import ContentFile
from django.http import FileResponse
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.shortcuts import render
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.crypto import get_random_string

# Local
from .forms import DeleteForm
from .forms import RecipientForm
from .models import Picture
from .models import Volunteer
from .tasks import build_email
from .tasks import send_email


# Root
def index(request):
    pictures = Picture.objects.all()
    return render(
        request,
        'app/index.html',
        context={
            'pictures': pictures,
        }
    )


# Authenticationa
def login(request):
    signup = request.GET.get('signup', None)
    request.session['signup'] = signup

    redirect_uri = request.build_absolute_uri(reverse('callback'))
    state = "{0}".format(
        get_random_string(),
    )
    request.session['state'] = state
    params = {
        'response_type': 'code',
        'client_id': settings.AUTH0_CLIENT_ID,
        'scope': 'openid profile email',
        'redirect_uri': redirect_uri,
        'state': state,
    }
    url = requests.Request(
        'GET',
        'https://{0}/authorize'.format(settings.AUTH0_DOMAIN),
        params=params,
    ).prepare().url
    return redirect(url)

def callback(request):
    # Reject if state doesn't match
    signup = request.session.get('signup', 'dashboard')
    browser_state = request.session.get('state', None)
    server_state = request.GET.get('state', None)
    if browser_state != server_state:
        return HttpResponse(status=400)

    # Get Auth0 Code
    code = request.GET.get('code', None)
    if not code:
        return HttpResponse(status=400)
    token_url = 'https://{0}/oauth/token'.format(
        settings.AUTH0_DOMAIN,
    )
    redirect_uri = request.build_absolute_uri(reverse('callback'))
    token_payload = {
        'client_id': settings.AUTH0_CLIENT_ID,
        'client_secret': settings.AUTH0_CLIENT_SECRET,
        'redirect_uri': redirect_uri,
        'code': code,
        'grant_type': 'authorization_code'
    }
    token_info = requests.post(
        token_url,
        data=json.dumps(token_payload),
        headers={
            'content-type': 'application/json',
        }
    ).json()
    user_url = 'https://{0}/userinfo?access_token={1}'.format(
        settings.AUTH0_DOMAIN,
        token_info.get('access_token', ''),
    )
    payload = requests.get(user_url).json()
    # format payload key
    payload['username'] = payload.pop('sub')
    user = authenticate(request, **payload)
    if user:
        log_in(request, user)
        return redirect(signup)
    return HttpResponse(status=403)

def logout(request):
    log_out(request)
    params = {
        'client_id': settings.AUTH0_CLIENT_ID,
        'return_to': request.build_absolute_uri(reverse('index')),
    }
    logout_url = requests.Request(
        'GET',
        'https://{0}/v2/logout'.format(settings.AUTH0_DOMAIN),
        params=params,
    ).prepare().url
    messages.success(
        request,
        "You Have Been Logged Out!",
    )
    return redirect(logout_url)

#Dashboard
@login_required
def dashboard(request):
    user = request.user
    return render(
        request,
        'app/dashboard.html',
        context={
            'user': user,
        }
    )

@login_required
def delete_user(request):
    if request.method == "POST":
        form = DeleteForm(request.POST)
        if form.is_valid():
            user = request.user
            user.delete()
            messages.error(
                request,
                "Account Deleted!",
            )
            return redirect('index')
    else:
        form = DeleteForm()
    return render(
        request,
        'app/user_delete.html',
        {'form': form,},
    )

# Footer
def about(request):
    return render(
        request,
        'app/about.html',
    )

def privacy(request):
    return render(
        request,
        'app/privacy.html',
    )

def delete(request):
    return render(
        request,
        'app/delete.html',
    )


# Recipient
# def recipients(request):
#     form = RecipientForm(
#         request.POST or None,
#     )
#     if form.is_valid():
#         recipient=form.save()
#         messages.success(
#             request,
#             "Submitted!",
#         )
#         email = build_email(
#             template='emails/confirmed.txt',
#             subject='Rake Up Eagle Confirmation',
#             context={'recipient': recipient},
#             to=[recipient.email],
#             from_email='Eagle Middle School PTO <eaglemiddlepto@gmail.com>',
#             bcc=['dbinetti@gmail.com', 'mnwashow@yahoo.com'],
#         )
#         send_email.delay(email)
#         return redirect('confirmation')
#     return render(
#         request,
#         'app/recipients.html',
#         context={
#             'form': form,
#         }
#     )

def confirmation(request):
    return render(
        request,
        'app/confirmation.html',
    )

# Volunteerl
def volunteer(request):
    return redirect(reverse('about'))


# def volunteers(request):
#     form = RecipientForm(
#         request.POST or None,
#     )
#     if form.is_valid():
#         recipient=form.save()
#         messages.success(
#             request,
#             "Submitted!",
#         )
#         email = build_email(
#             template='emails/confirmed.txt',
#             subject='Rake Up Eagle Confirmation',
#             context={'recipient': recipient},
#             to=[recipient.email],
#             from_email='Eagle Middle School PTO <eaglemiddlepto@gmail.com>',
#             bcc=['dbinetti@gmail.com', 'mnwashow@yahoo.com'],
#         )
#         send_email.delay(email)
#         return redirect('confirmation')
#     return render(
#         request,
#         'app/recipients.html',
#         context={
#             'form': form,
#         }
#     )

# Admin
def handouts(request):
    volunteers = Volunteer.objects.order_by(
        'last',
        'first',
    )
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
    volunteers = Volunteer.objects.order_by(
        'last',
        'first',
    )
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
    vs = Volunteer.objects.order_by(
        'last',
        'first',
    )

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
