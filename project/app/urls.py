# Django
from django.urls import path
from django.views.generic import TemplateView

# Local
from . import views

urlpatterns = [
    # Root
    path('', views.index, name='index',),
    path('faq/', views.faq, name='faq',),

    # Footer
    path('about/', TemplateView.as_view(template_name='app/pages/about.html'), name='about',),
    path('terms/', TemplateView.as_view(template_name='app/pages/terms.html'), name='terms',),
    path('support/', TemplateView.as_view(template_name='app/pages/support.html'), name='support',),
    path('donate/', TemplateView.as_view(template_name='app/pages/donate.html'), name='donate',),

    # Authentication
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('account/', views.account, name='account'),

    # Authentication
    path('send/', views.send, name='send',),
    path('verify/', views.verify, name='verify',),

    # Recipient
    path('recipient/', views.recipient, name='recipient',),
    path('team/', views.team, name='team',),
    path('success/', views.success, name='success',),

    # Twilio
    path('webhook', views.webhook, name='webhook',),

    # Admin
    path('dashboard/', views.dashboard, name='dashboard',),

    path('handout/<recipient_id>', views.handout, name='handout',),
    path('handout/<recipient_id>/pdf', views.handout_pdf, name='handout-pdf',),
    # path('handout/all', views.handout_pdfs, name='handouts',),
    path('csv/assignments/', views.export_assignments, name='export-assignments',),
    path('csv/recipients/', views.export_recipients, name='export-recipients',),
    path('csv/teams/', views.export_teams, name='export-teams',),
]
