# Django
from django.urls import path
from django.views.generic import TemplateView

# Local
from . import views

urlpatterns = [
    # Root
    path('', views.index, name='index',),

    # Footer
    path('about/', TemplateView.as_view(template_name='app/pages/about.html'), name='about',),
    path('privacy/', TemplateView.as_view(template_name='app/pages/privacy.html'), name='privacy',),
    path('terms/', TemplateView.as_view(template_name='app/pages/terms.html'), name='terms',),
    path('support/', TemplateView.as_view(template_name='app/pages/support.html'), name='support',),
    path('donate/', TemplateView.as_view(template_name='app/pages/donate.html'), name='donate',),
    path('faq/', TemplateView.as_view(template_name='app/pages/faq.html'), name='faq',),

    # Authentication
    path('login', views.login, name='login'),
    path('callback', views.callback, name='callback'),
    path('logout', views.logout, name='logout'),

    # Account
    path('account', views.account, name='account',),
    path('account/delete', views.account_delete, name='account-delete',),

    # Recipient
    path('recipient', views.recipient, name='recipient',),
    path('recipient/create', views.recipient_create, name='recipient-create',),
    path('recipient/delete', views.recipient_delete, name='recipient-delete',),

    # Teams
    path('teams', views.teams, name='teams',),

    path('volunteer', views.volunteer, name='volunteer',),
    path('volunteer/create', views.volunteer_create, name='volunteer-create',),
    path('volunteer/delete', views.volunteer_delete, name='volunteer-delete',),

    # Twilio
    path('sms', views.sms, name='sms',),

    # Admin
    path('call/', views.call, name='call',),
    path('dashboard/', views.dashboard, name='dashboard',),
    path('dashboard/<volunteer_id>', views.dashboard_volunteer, name='dashboard-volunteer',),
    # path('handout/', views.handouts, name='handouts',),
    # path('handout/<volunteer_id>', views.handout, name='handout',),
    # path('handout/<volunteer_id>', views.handout, name='handout',),
    # path('handout/<volunteer_id>/pdf', views.handout_pdf, name='handout_pdf',),
    # path('handouts/', views.handout_pdfs, name='handouts',),
    # path('csv/', views.export_csv, name='export_csv',),
]
