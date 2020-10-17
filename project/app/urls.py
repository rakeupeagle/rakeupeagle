# Django
from django.urls import path

# Local
from . import views

urlpatterns = [
    # Root
    path('', views.index, name='index',),
    # path('robots.txt', views.robots, name='robots',),
    # path('sitemap.txt', views.sitemap, name='sitemap',),

    # Authentication
    # path('login', views.login, name='login'),
    # path('signup/<kind>', views.signup, name='signup'),
    # path('callback', views.callback, name='callback'),
    # path('logout', views.logout, name='logout'),

    # Dashboard
    # path('dashboard', views.dashboard, name='dashboard',),
    path('volunteer/', views.volunteers, name='volunteers',),
    path('recipient/', views.recipients, name='recipients',),
    path('thanks/', views.thanks, name='thanks',),
    path('confirmation/', views.confirmation, name='confirmation',),
    # path('volunteer/<volunteer_id>', views.volunteer, name='volunteer',),
    # path('recipient/<recipient_id>', views.recipient, name='recipient',),

]
