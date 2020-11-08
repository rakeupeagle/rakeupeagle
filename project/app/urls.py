# Django
from django.urls import path

# Local
from . import views

urlpatterns = [
    # Root
    path('', views.index, name='index',),
    path('robots.txt', views.robots, name='robots',),
    path('sitemap.txt', views.sitemap, name='sitemap',),

    # Dashboard
    # path('recipient/', views.recipients, name='recipients',),
    # path('confirmation/', views.confirmation, name='confirmation',),
    # path('volunteer/', views.volunteers, name='volunteers',),
    # path('thanks/', views.thanks, name='thanks',),
    # path('volunteer/<volunteer_id>', views.volunteer, name='volunteer',),
    # path('recipient/<recipient_id>', views.recipient, name='recipient',),
]
