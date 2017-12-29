from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^user/registration$', views.register),
    url(r'^user/login$', views.login),
    url(r'^user/reroute$', views.reroute),
    url(r'^hangman/home$', views.hangman),
    url(r'^hangman/game$', views.game),
    url(r'^hangman/game/guess$', views.guess),
    url(r'^hangman/user/(?P<user_id>\d+)$', views.user_info),
    url(r'^hangman/new_word/(?P<user_id>\d+)$', views.new_word),
    url(r'^logout', views.logout)
]