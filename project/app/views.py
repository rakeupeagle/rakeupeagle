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
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from reversion.views import create_revision

from .decorators import validate_twilio_request
from .forms import AccountForm
from .forms import CallForm
from .forms import DeleteForm
from .forms import LoginForm
from .forms import RecipientForm
from .forms import RegisterForm
from .forms import TeamcallForm
from .forms import TeamForm
from .forms import VerifyCodeForm
from .models import Assignment
from .models import MessageArchive
from .models import Picture
from .models import Recipient
from .models import Team
from .models import User
# from .tasks import get_assignments_csv
from .tasks import check
from .tasks import send

# from .tasks import send_recipient_confirmation
# from .tasks import send_team_confirmation

log = logging.getLogger(__name__)

# Root
def index(request):
    pictures = Picture.objects.all()
    return render(
        request,
        'app/pages/index.html',
        context={
            'pictures': pictures,
            'is_active': True,
        }
    )


# Authentication
def login(request):
    form = LoginForm(request.POST or None)
    if form.is_valid():
        number = form.cleaned_data['phone'].as_e164
        try:
            user = User.objects.get(
                phone=number,
            )
        except User.DoesNotExist:
            request.session['number'] = number
            return redirect('register')
        user = authenticate(
            request,
            phone=number,
        )
        log_in(
            request,
            user,
            backend='app.backends.AppBackend',
        )
        messages.success(
            request,
            f"Welcome, {user.name}!",
        )
        return redirect('account')
    return render(
        request,
        'app/pages/login.html',
        context={
            'form': form,
        }
    )

def register(request):
    number = request.session.get('number', '')
    initial = {
        'phone': number,
    }
    form = RegisterForm(request.POST or None, initial=initial)
    if form.is_valid():
        number = form.cleaned_data['phone'].as_e164
        name = form.cleaned_data['name']
        user = authenticate(
            request,
            phone=number,
            name=name,
        )
        log_in(
            request,
            user,
            backend='app.backends.AppBackend',
        )
        messages.success(
            request,
            f"Welcome, {user.name}!",
        )
        return redirect('account')
    return render(
        request,
        'app/pages/register.html',
        context={
            'form': form,
        }
    )


def logout(request):
    log_out(request)
    messages.success(
        request,
        "You Have Been Logged Out!",
    )
    return redirect('index')


@login_required
def account(request):
    user = request.user
    if request.POST:
        form = AccountForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(
                request,
                'Saved!',
            )
            return redirect('account')
    form = AccountForm(instance=user)
    recipients = Recipient.objects.filter(
        user=request.user,
    )
    teams = Team.objects.filter(
        user=request.user,
    )
    return render(
        request,
        'app/pages/account.html',
        context={
            'user': user,
            'form': form,
            'recipients': recipients,
            'teams': teams,
        }
    )


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
        context={
            'form': form,
        },
    )

@login_required
def verification(request):
    return render(
        request,
        'app/pages/verification.html',
        context={
        },
    )

@login_required
def verify_send(request):
    send(
        request.user.phone.as_e164,
    )
    return redirect('verify-code')

@login_required
def verify_code(request):
    form = VerifyCodeForm(request.POST or None)
    if form.is_valid():
        code = form.cleaned_data.get('code')
        if check(request.user.phone.as_e164, code):
            request.user.is_verified = True
            request.user.save()
            messages.success(
                request,
                "Your account has been verified!",
            )
            return redirect('account')
    return render(
        request,
        'app/pages/verify_code.html',
        context={
            'form': form
        },
    )

# Recipient
@login_required
def recipient(request):
    recipient = request.user.recipients.first()
    if request.POST:
        form = RecipientForm(request.POST, instance=recipient)
    else:
        form = RecipientForm(instance=recipient)
    if form.is_valid():
        user = request.user
        recipient = form.save(commit=False)
        recipient.state = 0
        recipient.user = user
        recipient.save()
        messages.success(
            request,
            "Registration complete!  We will reach out before November 7th with futher details.",
        )
        send_recipient_confirmation(recipient)
    return render(
        request,
        'app/pages/recipient.html',
        context={
            'form': form,
        }
    )

@login_required
def team(request):
    team = request.user.teams.first()
    if request.POST:
        form = TeamForm(request.POST, instance=team)
    else:
        form = TeamForm(instance=team)
    if form.is_valid():
        user = request.user
        team = form.save(commit=False)
        team.state = 0
        team.user = user
        team.save()
        messages.success(
            request,
            "Registration complete!  We will reach out before November 7th with futher details.",
        )
        send_team_confirmation(team)
    else:
        print(form.errors)
    return render(
        request,
        'app/pages/team.html',
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
        team = Team.objects.order_by(
            'created',
        ).filter(
            admin_notes='',
            state=Team.STATE.new,
        ).earliest('created')
    except Team.DoesNotExist:
        messages.success(
            request,
            "All Teams Called for Now!",
        )
        return redirect('index')
    team.save()
    if request.POST:
        form = TeamcallForm(request.POST, instance=team)
        if form.is_valid():
            team = form.save(commit=False)
            team.confirm()
            team.save()
            messages.success(
                request,
                "Saved!",
            )
            return redirect('teamcall')
    else:
        form = TeamcallForm(instance=team)
    return render(
        request,
        'app/pages/teamcall.html',
        context = {
            'team': team,
            'form': form,
        },
    )

@staff_member_required
def dashboard(request):
    return render(
        request,
        'app/pages/dashboard.html',
    )

@staff_member_required
def dashboard_team(request, team_id):
    team = Team.objects.get(pk=team_id)
    return render(
        request,
        'app/pages/team.html',
        {'team': team},
    )

# @validate_twilio_request
# @csrf_exempt
# @require_POST
# def sms(request):
#     defaults = {}
#     raw = request.POST.dict()
#     sid = raw['SmsSid']
#     # status = getattr(Message.STATUS, raw.get('SmsStatus', Message.STATUS.new))
#     direction = Message.DIRECTION.inbound
#     to_phone = raw['To']
#     from_phone = raw['From']
#     body = raw['Body']
#     try:
#         user = User.objects.get(phone=from_phone)
#     except User.DoesNotExist:
#         log.error('no user')
#         return HttpResponse(status=404)
#     defaults = {
#         # 'status': status,
#         'direction': direction,
#         'to_phone': to_phone,
#         'from_phone': from_phone,
#         'body': body,
#         'user': user,
#         'raw': raw,
#     }
#     Message.objects.update_or_create(
#         sid=sid,
#         defaults=defaults,
#     )
#     return HttpResponse(status=201)

@staff_member_required
def handout_pdf(request, assignment_id):
    assignment = get_object_or_404(Assignment, pk=assignment_id)
    recipient = assignment.recipient
    team = assignment.team
    context={
        'recipient': recipient,
        'team': team,
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
        'team__name',
    )
    output = ''
    for assignment in assignments:
        context={
            'recipient': assignment.recipient,
            'team': assignment.team,
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
def export_assignments(request):
    response = HttpResponse('text/csv')
    response['Content-Disposition'] = 'attachment; filename=assignments.csv'
    gs = Assignment.objects.order_by(
        'team__name',
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
            g.team.name,
            g.team.phone.as_national,
            g.team.get_size_display(),
            g.recipient.name,
            g.recipient.phone.as_national,
            g.recipient.get_size_display(),
            g.recipient.location,
        ])
    return response


@staff_member_required
def export_recipients(request):
    response = HttpResponse('text/csv')
    response['Content-Disposition'] = 'attachment; filename=recipients.csv'
    recipients = Recipient.objects.filter(
        state=Recipient.STATE.new,
    ).order_by(
        'name',
    )
    writer = csv.writer(response)
    writer.writerow([
        'Name',
        'Phone',
        'Location',
        'Size',
        'Notes',
        'Admin',
    ])
    for recipient in recipients:
        try:
            phone = recipient.phone.as_national
        except AttributeError:
            phone = None
        writer.writerow([
            recipient.name,
            phone,
            recipient.location,
            recipient.get_size_display(),
            recipient.public_notes,
            # recipient.admin_notes,
        ])
    return response


@staff_member_required
def export_teams(request):
    response = HttpResponse('text/csv')
    response['Content-Disposition'] = 'attachment; filename=teams.csv'
    teams = Team.objects.filter(
        state=Team.STATE.new,
    ).order_by(
        'name',
    )
    writer = csv.writer(response)
    writer.writerow([
        'Name',
        'Phone',
        'Nickname',
        'Size',
        'Notes',
        'Admin',
    ])
    for team in teams:
        writer.writerow([
        team.name,
        team.phone,
        team.nickname,
        team.get_size_display(),
        team.public_notes,
        # team.admin_notes,
    ])
    return response
