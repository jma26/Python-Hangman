from django.conf.urls import urls
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^user/registration$', views.register),
    url(r'^user/login$', views.login)
]