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

from .decorators import twilio
from .forms import AccountForm
from .forms import CallForm
from .forms import DeleteForm
from .forms import RecipientForm
from .forms import VolunteerForm
from .models import Account
from .models import Message
from .models import Picture
from .models import Recipient
from .models import Volunteer
from .tasks import send_recipient_confirmation
from .tasks import send_volunteer_confirmation

log = logging.getLogger(__name__)

# Root
def index(request):
    if request.user.is_authenticated:
        return redirect('account')
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
    # next_url = server_state.partition('|')[2]

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
        if initial == 'recipient':
            return redirect('recipient-create')
        if initial == 'volunteer':
            return redirect('volunteer-create')
        if user.is_admin:
            return redirect('admin:index')
        # cookies = request.COOKIES
        # gen = next(v for (k,v) in cookies.items() if k.startswith('ph'))
        # posthog_dict = json.loads(urllib.parse.unquote(gen))
        # distinct_id =  posthog_dict.get('distinct_id')

        # if distinct_id:
            # posthog.identify(
                # distinct_id, {
                # 'name': str(user.phone),
            # })
        # if (user.last_login - user.created) < datetime.timedelta(minutes=1):
        #     messages.success(
        #         request,
        #         "Welcome! Thank you for joining!"
        #     )
        #     messages.warning(
        #         request,
        #         "Next, please update your details below."
        #     )
        #     return redirect('volunteer')
        # Otherwise, redirect to next_url, defaults to 'account'
        # messages.success(
        #     request,
        #     "Welcome Back!"
        # )
        # return redirect(next_url)
        return redirect('account')
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

#Account
@login_required
def account(request):
    account = request.user.account
    recipient = getattr(account, 'recipient', None)
    volunteer = getattr(account, 'volunteer', None)
    form = AccountForm(request.POST, instance=account) if request.POST else AccountForm(instance=account)
    if form.is_valid():
        form.save()
        messages.success(
            request,
            "Saved!",
        )
        return redirect('account')
    return render(
        request,
        'app/pages/account.html',
        context={
            'account': account,
            'recipient': recipient,
            'volunteer': volunteer,
            'form': form,
        }
    )

@login_required
def account_delete(request):
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
        'app/pages/account_delete.html',
        {'form': form,},
    )

# Recipient
@login_required
def recipient(request):
    account = request.user.account
    recipient = getattr(account, 'recipient', None)
    form = RecipientForm(request.POST, instance=recipient) if request.POST else RecipientForm(instance=recipient)
    if form.is_valid():
        recipient = form.save(commit=False)
        recipient.account = account
        recipient.save()
        send_recipient_confirmation.delay(recipient)
        messages.success(
            request,
            "Saved!",
        )
        return redirect('account')
    return render(
        request,
        'app/pages/recipient.html',
        context={
            'form': form,
        }
    )

@login_required
def recipient_create(request):
    account = request.user.account
    recipient = getattr(account, 'recipient', None)
    if recipient:
        return redirect('account')
    account_form = AccountForm(request.POST, instance=account) if request.POST else AccountForm(instance=account)
    recipient_form = RecipientForm(request.POST) if request.POST else RecipientForm(instance=recipient)
    if account_form.is_valid() and recipient_form.is_valid():
        account_form.save()
        recipient = recipient_form.save(commit=False)
        recipient.account = account
        recipient.save()
        send_recipient_confirmation.delay(recipient)
        messages.success(
            request,
            "Registration complete!  We will reach out before November 8th with futher details.",
        )
        return redirect('account')
    return render(
        request,
        'app/pages/recipient_create.html',
        context={
            'account_form': account_form,
            'recipient_form': recipient_form,
        }
    )

@login_required
def recipient_delete(request):
    if request.method == "POST":
        form = DeleteForm(request.POST)
        if form.is_valid():
            recipient = getattr(request.user.account, 'recipient', None)
            if recipient:
                recipient.delete()
            messages.error(
                request,
                "Removed!",
            )
            return redirect('account')
    else:
        form = DeleteForm()
    return render(
        request,
        'app/pages/recipient_delete.html',
        {'form': form,},
    )


# Volunteer
@login_required
def volunteer(request):
    account = request.user.account
    volunteer = getattr(account, 'volunteer', None)
    form = VolunteerForm(request.POST, instance=volunteer) if request.POST else VolunteerForm(instance=volunteer)
    if form.is_valid():
        volunteer = form.save(commit=False)
        volunteer.account = account
        volunteer.save()
        send_volunteer_confirmation.delay(volunteer)
        messages.success(
            request,
            "Saved!",
        )
        return redirect('account')
    return render(
        request,
        'app/pages/volunteer.html',
        context={
            'form': form,
        }
    )

@login_required
def volunteer_create(request):
    account = request.user.account
    volunteer = getattr(account, 'volunteer', None)
    if volunteer:
        return redirect('account')
    account_form = AccountForm(request.POST, instance=account) if request.POST else AccountForm(instance=account)
    volunteer_form = VolunteerForm(request.POST) if request.POST else VolunteerForm(instance=volunteer)
    if account_form.is_valid() and volunteer_form.is_valid():
        account_form.save()
        volunteer = volunteer_form.save(commit=False)
        volunteer.account = account
        volunteer.save()
        send_volunteer_confirmation.delay(volunteer)
        messages.success(
            request,
            "Registration complete!  We will reach out before November 8th with futher details.",
        )
        return redirect('account')
    return render(
        request,
        'app/pages/volunteer_create.html',
        context={
            'account_form': account_form,
            'volunteer_form': volunteer_form,
        }
    )

@login_required
def volunteer_delete(request):
    if request.method == "POST":
        form = DeleteForm(request.POST)
        if form.is_valid():
            volunteer = getattr(request.user.account, 'volunteer', None)
            if volunteer:
                volunteer.delete()
            messages.error(
                request,
                "You have been removed as a Volunteer!",
            )
            return redirect('account')
    else:
        form = DeleteForm()
    return render(
        request,
        'app/pages/volunteer_delete.html',
        {'form': form,},
    )


# Admin
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
        return redirect('account')
    recipient.pend()
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
    account = Account.objects.filter(phone=from_phone).first()
    defaults = {
        # 'status': status,
        'direction': direction,
        'to_phone': to_phone,
        'from_phone': from_phone,
        'body': body,
        'account': account,
        'raw': raw,
    }
    Message.objects.update_or_create(
        sid=sid,
        defaults=defaults,
    )
    return HttpResponse(status=201)


@staff_member_required
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

@staff_member_required
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

@staff_member_required
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
