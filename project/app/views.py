import csv
import datetime
import logging

import jwt
import pydf
import requests
from django.conf import settings
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
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
from reversion.views import create_revision

from .decorators import twilio
from .forms import CallForm
from .forms import DeleteForm
from .forms import RecipientForm
from .forms import TeamcallForm
from .forms import VolunteerForm
from .models import Assignment
from .models import Event
from .models import Message
from .models import Picture
from .models import Recipient
from .models import User
from .models import Volunteer
from .tasks import get_assignments_csv
from .tasks import send_recipient_confirmation
from .tasks import send_volunteer_confirmation

log = logging.getLogger(__name__)

# Root
def index(request):
    pictures = Picture.objects.all()
    return render(
        request,
        'app/pages/index.html',
        context={
            'pictures': pictures,
            'is_active': settings.ACTIVE,
        }
    )

# Authentication
def login(request):
    # Set landing page depending on initial button
    initial = request.GET.get('initial', 'None')
    redirect_uri = request.build_absolute_uri(reverse('callback'))
    state = f"{initial}|{get_random_string()}"
    request.session['state'] = state

    params = {
        'response_type': 'code',
        'client_id': settings.AUTH0_CLIENT_ID,
        'scope': 'openid phone',
        'redirect_uri': redirect_uri,
        'state': state,
        'initial_screen': 'login',
    }
    url = requests.Request(
        'GET',
        f'https://{settings.AUTH0_DOMAIN}/authorize',
        params=params,
    ).prepare().url
    return redirect(url)


def callback(request):
    # Reject if state doesn't match
    browser_state = request.session.get('state')
    server_state = request.GET.get('state')
    if browser_state != server_state:
        del request.session['state']
        log.error('state mismatch')
        messages.error(
            request,
            "Sorry, there was a problem.  Please try again or contact support."
        )
        return redirect('index')

    # get initial
    initial = browser_state.partition("|")[0]

    # Get Auth0 Code
    code = request.GET.get('code', None)
    if not code:
        log.error('no code')
        return HttpResponse(status=400)
    token_url = f'https://{settings.AUTH0_DOMAIN}/oauth/token'
    redirect_uri = request.build_absolute_uri(reverse('callback'))
    token_payload = {
        'client_id': settings.AUTH0_CLIENT_ID,
        'client_secret': settings.AUTH0_CLIENT_SECRET,
        'code': code,
        'grant_type': 'authorization_code',
        'redirect_uri': redirect_uri,
    }
    token = requests.post(
        token_url,
        json=token_payload,
    ).json()
    payload = jwt.decode(
        token['id_token'],
        audience=settings.AUTH0_CLIENT_ID,
        options={
            'verify_signature': False,
        }
    )
    payload['username'] = payload.pop('sub')
    payload['phone'] = payload.pop('phone_number')
    payload['name'] = ''
    user = authenticate(request, **payload)
    if user:
        log_in(request, user)
        if user.is_admin:
            return redirect('admin:index')
        is_recipient = [
            initial == 'recipient',
            user.recipients.filter(
                event__state=Event.STATE.active,
            ),
        ]
        is_volunteer = [
            initial == 'volunteer',
            user.volunteers.filter(
                event__state=Event.STATE.active,
            ),
        ]
        if any(is_recipient):
            return redirect('recipient')
        if any(is_volunteer):
            return redirect('volunteer')
    log.error('callback fallout')
    return HttpResponse(status=403)


def logout(request):
    log_out(request)
    params = {
        'client_id': settings.AUTH0_CLIENT_ID,
        'return_to': request.build_absolute_uri(reverse('index')),
    }
    logout_url = requests.Request(
        'GET',
        f'https://{settings.AUTH0_DOMAIN}/v2/logout',
        params=params,
    ).prepare().url
    messages.success(
        request,
        "You Have Been Logged Out!",
    )
    return redirect(logout_url)

@login_required
def delete(request):
    form = DeleteForm(request.POST or None)
    if form.is_valid():
        user = request.user
        user.delete()
        messages.error(
            request,
            "Account Deleted!",
        )
        return redirect('index')
    return render(
        request,
        'app/pages/delete.html',
        {'form': form,},
    )

# Recipient
@login_required
def recipient(request):
    user = request.user
    recipient, created = Recipient.objects.get_or_create(
        event__state=Event.STATE.active,
        user=user,
    )
    form = RecipientForm(request.POST, instance=recipient) if request.POST else RecipientForm(instance=recipient)
    if form.is_valid():
        recipient = form.save()
        if created:
            send_recipient_confirmation.delay(recipient)
        messages.success(
            request,
            "Registration complete!  We will reach out before November 8th with futher details.",
        )
    return render(
        request,
        'app/pages/recipient.html',
        context={
            'form': form,
        }
    )

@login_required
def volunteer(request):
    user = request.user
    volunteer, created = Volunteer.objects.get_or_create(
        event__state=Event.STATE.active,
        user=user,
    )
    form = VolunteerForm(request.POST, instance=volunteer) if request.POST else VolunteerForm(instance=volunteer)
    if form.is_valid():
        volunteer = form.save()
        if created:
            send_volunteer_confirmation.delay(volunteer)
        messages.success(
            request,
            "Registration complete!  We will reach out before November 8th with futher details.",
        )
    return render(
        request,
        'app/pages/volunteer.html',
        context={
            'form': form,
        }
    )



# Admin
@login_required
@create_revision()
def call(request):
    try:
        recipient = Recipient.objects.order_by(
            'created',
        ).filter(
            admin_notes='',
            state=Recipient.STATE.new,
        ).earliest('created')
    except Recipient.DoesNotExist:
        messages.success(
            request,
            "All Recipients Called for Now!",
        )
        return redirect('index')
    recipient.save()
    if request.POST:
        form = CallForm(request.POST, instance=recipient)
        if form.is_valid():
            recipient = form.save(commit=False)
            recipient.confirm()
            recipient.save()
            messages.success(
                request,
                "Saved!",
            )
            return redirect('call')
    else:
        form = CallForm(instance=recipient)
    return render(
        request,
        'app/pages/call.html',
        context = {
            'recipient': recipient,
            'form': form,
        },
    )

@login_required
@create_revision()
def teamcall(request):
    try:
        volunteer = Volunteer.objects.order_by(
            'created',
        ).filter(
            admin_notes='',
            state=Volunteer.STATE.new,
        ).earliest('created')
    except Volunteer.DoesNotExist:
        messages.success(
            request,
            "All Volunteers Called for Now!",
        )
        return redirect('index')
    volunteer.save()
    if request.POST:
        form = TeamcallForm(request.POST, instance=volunteer)
        if form.is_valid():
            volunteer = form.save(commit=False)
            volunteer.confirm()
            volunteer.save()
            messages.success(
                request,
                "Saved!",
            )
            return redirect('teamcall')
    else:
        form = TeamcallForm(instance=volunteer)
    return render(
        request,
        'app/pages/teamcall.html',
        context = {
            'volunteer': volunteer,
            'form': form,
        },
    )

@staff_member_required
def dashboard(request):
    volunteers = Volunteer.objects.order_by(
        # 'last_name',
        # 'first_name',
    )
    return render(
        request,
        'app/pages/dashboard.html',
        {'volunteers': volunteers},
    )

@staff_member_required
def dashboard_volunteer(request, volunteer_id):
    volunteer = Volunteer.objects.get(pk=volunteer_id)
    return render(
        request,
        'app/pages/volunteer.html',
        {'volunteer': volunteer},
    )

@twilio
def sms(request):
    defaults = {}
    raw = request.POST.dict()
    sid = raw['SmsSid']
    # status = getattr(Message.STATUS, raw.get('SmsStatus', Message.STATUS.new))
    direction = Message.DIRECTION.inbound
    to_phone = raw['To']
    from_phone = raw['From']
    body = raw['Body']
    user = User.objects.filter(phone=from_phone).first()
    defaults = {
        # 'status': status,
        'direction': direction,
        'to_phone': to_phone,
        'from_phone': from_phone,
        'body': body,
        'user': user,
        'raw': raw,
    }
    Message.objects.update_or_create(
        sid=sid,
        defaults=defaults,
    )
    return HttpResponse(status=201)

@staff_member_required
def handout_pdf(request, assignment_id):
    assignment = get_object_or_404(Assignment, pk=assignment_id)
    recipient = assignment.recipient
    volunteer = assignment.volunteer
    context={
        'recipient': recipient,
        'volunteer': volunteer,
    }
    rendered = render_to_string('app/pdfs/handout.html', context)
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

@staff_member_required
def handout_pdfs(request):
    assignments = Assignment.objects.order_by(
        'volunteer__name',
    )
    output = ''
    for assignment in assignments:
        context={
            'recipient': assignment.recipient,
            'volunteer': assignment.volunteer,
        }
        rendered = render_to_string('app/pdfs/handout.html', context)
        output += '<div class="new-page"></div>'+rendered
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

@staff_member_required
def export_csv(request):
    response = HttpResponse('text/csv')
    response['Content-Disposition'] = 'attachment; filename=assignments.csv'
    gs = Assignment.objects.order_by(
        'volunteer__name',
    )
    writer = csv.writer(response)
    writer.writerow([
        'Team Leader',
        'Team Phone',
        'Team Size',
        'Recipient Name',
        'Recipient Phone',
        'Recipient Size',
        'Recipient Location',
    ])
    for g in gs:
        writer.writerow([
            g.volunteer.name,
            g.volunteer.phone.as_national,
            g.volunteer.get_size_display(),
            g.recipient.name,
            g.recipient.phone.as_national,
            g.recipient.get_size_display(),
            g.recipient.location,
        ])
    return response
