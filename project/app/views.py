import csv
import datetime
import logging

# import pydf
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
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from phonenumber_field.phonenumber import PhoneNumber
from weasyprint import HTML

from .decorators import validate_twilio_request
# from .forms import DeleteForm
from .forms import AccountForm
from .forms import CallForm
from .forms import LoginForm
from .forms import RecipientForm
from .forms import TeamcallForm
from .forms import TeamForm
from .forms import VerifyCodeForm
# from .tasks import get_assignments_csv
from .helpers import check
from .helpers import inbound_message
from .helpers import send as send_code
# from .models import Message
from .models import Assignment
from .models import Event
from .models import Message
from .models import Recipient
from .models import Team
from .models import User

log = logging.getLogger(__name__)

# Root
def index(request):
    try:
        event = Event.objects.get(
            state=Event.StateChoices.CURRENT,
        )
        is_closed = datetime.date.today() > event.deadline
    except Event.DoesNotExist:
        event = None
        is_closed = True
    return render(
        request,
        'app/pages/index.html',
        context={
            'event': event,
            'is_closed': is_closed,
        }
    )


def faq(request):
    try:
        event = Event.objects.get(
            state=Event.StateChoices.CURRENT,
        )
    except Event.DoesNotExist:
        event = None
    return render(
        request,
        'app/pages/faq.html',
        context={
            'event': event,
        }
    )


# Authentication
def login(request):
    if request.user.is_authenticated:
        return redirect('account')
    form = LoginForm(request.POST or None)
    if form.is_valid():
        number = form.cleaned_data['phone'].as_e164
        initial = request.GET.get('next', 'account')
        request.session['number'] = number
        request.session['initial'] = initial
        send_code(
            number,
        )
        return redirect('verify')
    return render(
        request,
        'app/pages/login.html',
        context={
            'form': form,
        }
    )


def send(request):
    number = request.session['number']
    send_code(
        number,
    )
    return redirect('verify')


def verify(request):
    form = VerifyCodeForm(request.POST or None)
    number = request.session['number']
    initial = request.session['initial']
    phone = PhoneNumber.from_string(number)
    if form.is_valid():
        code = form.cleaned_data.get('code')
        if check(number, code):
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
                "You have logged in!",
            )
            return redirect(initial)
        messages.warning(
            request,
            "Sorry, that code didn't work.  Try again.",
        )
    return render(
        request,
        'app/pages/verify.html',
        context={
            'form': form,
            'phone': phone,
        },
    )


def logout(request):
    log_out(request)
    messages.success(
        request,
        "You Have Been Logged Out!",
    )
    return redirect('index')


# Account
@login_required
def account(request):
    user = request.user
    if user.is_admin:
        return redirect('app:dashboard')
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


def recipient(request):
    event = Event.objects.get(
        state=Event.StateChoices.CURRENT,
    )
    form = RecipientForm(request.POST or None)
    if form.is_valid():
        name = form.cleaned_data['name']
        location = form.cleaned_data['location']
        size = form.cleaned_data['size']
        is_veteran = form.cleaned_data['is_veteran']
        is_senior = form.cleaned_data['is_senior']
        is_disabled = form.cleaned_data['is_disabled']
        public_notes = form.cleaned_data['public_notes']
        phone = form.cleaned_data['phone']
        place_id = form.cleaned_data['place_id']
        point = form.cleaned_data['point']
        user, _ = User.objects.update_or_create(
            phone=form.cleaned_data['phone'],
            defaults={
                'name': form.cleaned_data['name'],
            }
        )
        try:
            recipient = Recipient.objects.get(
                place_id=place_id,
                event=event,
            )
            recipient.name = name
            recipient.location = location
            recipient.size = size
            recipient.is_veteran = is_veteran
            recipient.is_senior = is_senior
            recipient.is_disabled = is_disabled
            recipient.public_notes = public_notes
            recipient.phone = phone
            recipient.point = point
        except Recipient.DoesNotExist:
            recipient = form.save(commit=False)
        recipient.event = event
        recipient.user = user
        recipient.save()
        messages.success(
            request,
            "Saved!",
        )
        return redirect('success')
    else:
        messages.warning(
            request,
            form.errors,
        )
    return render(
        request,
        'app/pages/recipient.html',
        context={
            'form': form,
            'GOOGLE_API_KEY': settings.GOOGLE_API_KEY,
            'event': event,
        }
    )


def team(request):
    form = TeamForm(request.POST or None)
    event = Event.objects.get(
        state=Event.StateChoices.CURRENT,
    )
    if form.is_valid():
        phone = form.cleaned_data['phone']
        name = form.cleaned_data['name']
        nickname = form.cleaned_data['nickname']
        size = form.cleaned_data['size']
        public_notes = form.cleaned_data['public_notes']
        user, _ = User.objects.update_or_create(
            phone=phone,
            defaults={
                'name': name,
            }
        )
        try:
            team = Team.objects.get(
                phone=phone,
                event=event,
            )
            team.name = name
            team.nickname = nickname
            team.size = size
            team.public_notes = public_notes
        except Team.DoesNotExist:
            team = form.save(commit=False)
        team.event = event
        team.user = user
        team.save()
        messages.success(
            request,
            "Saved!",
        )
        return redirect('success')
    else:
        messages.warning(
            request,
            form.errors,
        )
    return render(
        request,
        'app/pages/team.html',
        context={
            'form': form,
            'event': event,
        }
    )


def success(request):
    return render(
        request,
        'app/pages/success.html',
    )


# Admin
@staff_member_required
def dashboard(request):
    teams = Team.objects.filter(
        state__in=[
            Team.StateChoices.NEW,
            Team.StateChoices.ACCEPTED,
        ],
    )
    recipients = Recipient.objects.filter(
        state__in=[
            Recipient.StateChoices.NEW,
            Recipient.StateChoices.ACCEPTED,
        ],
    )

    return render(
        request,
        'app/pages/dashboard.html',
        context = {
            'teams': teams,
            'recipients': recipients,
        },
    )


@staff_member_required
def admin_recipient(request, recipient_id):
    recipient = get_object_or_404(Recipient, pk=recipient_id)
    messages = recipient.messages.order_by(
        '-created',
    )
    transitions = sorted(
        recipient.get_available_state_transitions(),
        key=lambda x: x.target.value,
        reverse=True,
    )
    return render(
        request,
        'app/pages/admin_recipient.html',
        context = {
            'recipient': recipient,
            'texts': messages,
            'transitions': transitions,
        },
    )



@staff_member_required
def admin_team(request, team_id):
    team = get_object_or_404(Team, pk=team_id)
    messages = team.messages.order_by(
        '-created',
    )
    transitions = sorted(
        team.get_available_state_transitions(),
        key=lambda x: x.target.value,
        reverse=True,
    )
    return render(
        request,
        'app/pages/admin_team.html',
        context = {
            'team': team,
            'texts': messages,
            'transitions': transitions,
        },
    )



@staff_member_required
def admin_team_action(request, team_id, action):
    team = get_object_or_404(Team, pk=team_id)
    invoke = getattr(team, action)
    invoke()
    team.save()
    messages.success(
        request,
        f"{team.get_state_display()}!",
    )
    return redirect('admin-team', team_id)


@staff_member_required
def admin_recipient_action(request, recipient_id, action):
    recipient = get_object_or_404(Team, pk=recipient_id)
    invoke = getattr(recipient, action)
    invoke()
    recipient.save()
    messages.success(
        request,
        f"{recipient.get_state_display()}!",
    )
    return redirect('admin-recipient', recipient_id)


@staff_member_required
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


@staff_member_required
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
def export_assignments(request):
    response = HttpResponse('text/csv')
    response['Content-Disposition'] = 'attachment; filename=assignments.csv'
    gs = Assignment.objects.filter(
        event__year=2024,
    ).order_by(
        'rake__team__user__name',
    )
    writer = csv.writer(response)
    writer.writerow([
        'Team Leader',
        'Team Phone',
        'Team Size',
        'Recipient Name',
        'Recipient Phone',
        'Recipient Veteran',
        'Recipient Size',
        'Recipient Location',
    ])
    for g in gs:
        writer.writerow([
            g.rake.team.user.name,
            g.rake.team.user.phone.as_national,
            g.rake.team.get_size_display(),
            g.yard.recipient.user.name,
            g.yard.recipient.user.phone.as_national,
            g.yard.recipient.is_veteran,
            g.yard.recipient.get_size_display(),
            g.yard.recipient.location,
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


@staff_member_required
def handout(request, recipient_id):
    recipient = get_object_or_404(Recipient, pk=recipient_id)
    context={
        'recipient': recipient,
    }
    return render(
        request,
        'app/pdfs/handout.html',
        context = {
            'recipient': recipient,
        },
    )


@staff_member_required
def handout_pdf(request, recipient_id):
    recipient = get_object_or_404(Recipient, pk=recipient_id)
    context={
        'recipient': recipient,
    }
    string = render_to_string('app/pdfs/handout.html', context)
    html = HTML(string=string)
    pdf = html.write_pdf()
    content = ContentFile(pdf)
    return FileResponse(
        content,
        as_attachment=True,
        filename='rake_up_eagle_handout.pdf',
    )


# @staff_member_required
# def handout_pdfs(request):
#     assignments = Assignment.objects.order_by(
#         'team__name',
#     )
#     output = ''
#     for assignment in assignments:
#         context={
#             'recipient': assignment.recipient,
#             'team': assignment.team,
#         }
#         rendered = render_to_string('app/pdfs/handout.html', context)
#         output += '<div class="new-page"></div>'+rendered
#     pdf = pydf.generate_pdf(
#         output,
#         enable_smart_shrinking=False,
#         orientation='Portrait',
#         margin_top='10mm',
#         margin_bottom='10mm',
#     )
#     content = ContentFile(pdf)
#     return FileResponse(
#         content,
#         as_attachment=True,
#         filename='handouts.pdf',
#     )


# Webhook
@validate_twilio_request
@csrf_exempt
@require_POST
def webhook(request):
    data = request.POST.dict()
    inbound_message(data)
    return HttpResponse(status=200)
