from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^user/registration$', views.register),
    url(r'^user/login$', views.login),
    url(r'^user/reroute', views.reroute),
    url(r'^hangman', views.hangman)
]