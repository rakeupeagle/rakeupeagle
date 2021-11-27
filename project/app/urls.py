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
    path('delete', views.delete, name='delete',),

    # Recipient
    path('account', views.account, name='account',),
    path('recipient', views.recipient, name='recipient',),
    path('team', views.team, name='team',),

    # Twilio
    path('sms', views.sms, name='sms',),

    # Admin
    path('dashboard/', views.dashboard, name='dashboard',),
    path('dashboard/<team_id>', views.dashboard_team, name='dashboard-team',),
    path('assignment/<assignment_id>/pdf', views.handout_pdf, name='handout_pdf',),
    path('handouts/', views.handout_pdfs, name='handouts',),
    path('csv/', views.export_csv, name='export_csv',),
]
