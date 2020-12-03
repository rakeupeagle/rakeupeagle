# Django
from django.urls import path

# Local
from . import views

urlpatterns = [
    # Root
    path('', views.index, name='index',),

    # Authentication
    path('login', views.login, name='login'),
    path('callback', views.callback, name='callback'),
    path('logout', views.logout, name='logout'),

    # Dashboard
    path('dashboard', views.dashboard, name='dashboard',),

    # Dashboard
    # path('recipient/', views.recipients, name='recipients',),
    # path('confirmation/', views.confirmation, name='confirmation',),
    # path('volunteer/', views.volunteers, name='volunteers',),
    path('handout/', views.handouts, name='handouts',),
    path('handout/<volunteer_id>/pdf', views.handout_pdf, name='handout_pdf',),
    path('handout/<volunteer_id>', views.handout, name='handout',),
    path('handouts/', views.handout_pdfs, name='handouts',),
    path('csv/', views.export_csv, name='export_csv',),
    # path('thanks/', views.thanks, name='thanks',),
    # path('volunteer/<volunteer_id>', views.volunteer, name='volunteer',),
    # path('recipient/<recipient_id>', views.recipient, name='recipient',),
]
