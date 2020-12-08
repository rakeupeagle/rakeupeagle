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
    # path('recipient/', views.recipients, name='recipients',),
    # path('confirmation/', views.confirmation, name='confirmation',),

    # Volunteer
    path('volunteer/', views.volunteer, name='volunteer',),

    # Admin
    path('handout/', views.handouts, name='handouts',),
    path('handout/<volunteer_id>', views.handout, name='handout',),
    path('handout/<volunteer_id>/pdf', views.handout_pdf, name='handout_pdf',),
    path('handouts/', views.handout_pdfs, name='handouts',),
    path('csv/', views.export_csv, name='export_csv',),
]
