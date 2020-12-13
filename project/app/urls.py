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
    path('dashboard/delete', views.delete_user, name='delete-user',),

    # Footer
    path('about/', views.about, name='about',),
    path('privacy/', views.privacy, name='privacy',),
    path('support/', views.support, name='support',),
    path('delete/', views.delete, name='delete',),

    # Recipient
    path('recipient/create', views.recipient_create, name='recipient',),
    path('recipient/confirmation', views.recipient_confirmation, name='recipient-confirmation',),
    path('recipient/update', views.recipient_update, name='recipient-update',),
    path('recipient/delete', views.recipient_delete, name='recipient-delete',),

    # Volunteer
    path('volunteer/create', views.volunteer_create, name='volunteer',),
    path('volunteer/confirmation', views.volunteer_confirmation, name='volunteer-confirmation',),
    path('volunteer/update', views.volunteer_update, name='volunteer-update',),
    path('volunteer/delete', views.volunteer_delete, name='volunteer-delete',),


    # Admin
    path('handout/', views.handouts, name='handouts',),
    path('handout/<volunteer_id>', views.handout, name='handout',),
    path('handout/<volunteer_id>/pdf', views.handout_pdf, name='handout_pdf',),
    path('handouts/', views.handout_pdfs, name='handouts',),
    path('csv/', views.export_csv, name='export_csv',),
]
