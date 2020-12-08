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
from .forms import VolunteerForm
from .models import Picture
from .models import Volunteer
from .tasks import build_email
from .tasks import send_email


# Root
def index(request):
    pictures = Picture.objects.all()
    return render(
        request,
        'app/pages/index.html',
        context={
            'pictures': pictures,
        }
    )


# Authentication
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
        'initial_screen': 'login', # signUp
    }
    url = requests.Request(
        'GET',
        'https://{0}/authorize'.format(settings.AUTH0_DOMAIN),
        params=params,
    ).prepare().url
    return redirect(url)

def callback(request):
    # Reject if state doesn't match
    # signup = request.session.get('signup', 'dashboard')
    signup = 'volunteer-create'
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
        'app/pages/dashboard.html',
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
        'app/pages/user_delete.html',
        {'form': form,},
    )

# Footer
def about(request):
    return render(
        request,
        'app/pages/about.html',
    )

def privacy(request):
    return render(
        request,
        'app/pages/privacy.html',
    )

def support(request):
    return render(
        request,
        'app/pages/support.html',
    )

def delete(request):
    return render(
        request,
        'app/pages/delete.html',
    )


# Recipient
@login_required
def recipient_create(request):
    data = {
        'name': request.user.name,
        'email': request.user.email,
    }
    if request.POST:
        form = RecipientForm(request.POST)
    else:
        form = RecipientForm(initial=data)
    if form.is_valid():
        form.save()
        messages.success(
            request,
            "Submitted!",
        )
        return redirect('recipient-confirmation')
    return render(
        request,
        'app/pages/recipient.html',
        context={
            'form': form,
        }
    )

@login_required
def recipient_confirmation(request):
    return render(
        request,
        'app/pages/recipient_confirmation.html',
    )

@login_required
def recipient_update(request, recipient_id):
    recipient = Recipient.objects.get(id=recipient_id)
    if request.POST:
        form = RecipientForm(request.POST, instance=recipient)
    else:
        form = RecipientForm(instance=recipient)
    if form.is_valid():
        form.save()
        messages.success(
            request,
            "Saved!",
        )
        return redirect('recipient-update', recipient_id=recipient_id)
    return render(
        request,
        'app/pages/recipient.html',
        context={
            'form': form,
        }
    )

# Volunteer
@login_required
def volunteer_create(request):
    data = {
        'name': request.user.name,
        'email': request.user.email,
    }
    if request.POST:
        form = VolunteerForm(request.POST)
    else:
        form = VolunteerForm(initial=data)
    if form.is_valid():
        form.save()
        messages.success(
            request,
            "Submitted!",
        )
        return redirect('confirmation')
    return render(
        request,
        'app/pages/volunteer.html',
        context={
            'form': form,
        }
    )

@login_required
def volunteer_confirmation(request):
    return render(
        request,
        'app/pages/volunteer_confirmation.html',
    )

@login_required
def volunteer_update(request, volunteer_id):
    volunteer = Volunteer.objects.get(id=volunteer_id)
    if request.POST:
        form = VolunteerForm(request.POST, instance=volunteer)
    else:
        form = VolunteerForm(instance=volunteer)
    if form.is_valid():
        form.save()
        messages.success(
            request,
            "Saved!",
        )
        return redirect('volunteer-update', volunteer_id=volunteer_id)
    return render(
        request,
        'app/pages/volunteer.html',
        context={
            'form': form,
        }
    )


# Admin
def handouts(request):
    volunteers = Volunteer.objects.order_by(
        'last',
        'first',
    )
    return render(
        request,
        'app/pages/handouts.html',
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
        'app/pages/handout.html',
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
    rendered = render_to_string('app/pages/handout.html', context)
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
        rendered = render_to_string('app/pages/handout.html', context)
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
