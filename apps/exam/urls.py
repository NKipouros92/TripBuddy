from django.conf.urls import url
from . import views           

urlpatterns = [
    url(r'^$', views.index),
    url(r'^index$', views.index),
    url(r'^create$', views.create),
    url(r'^new$', views.new),
    url(r'^addTrip$', views.addTrip),
    url(r'^join/(?P<id>\d+)$', views.join),
    url(r'^show/(?P<id>\d+)$', views.show),
    url(r'^login$', views.login),
    url(r'^logout$', views.logout),
    url(r'^success$', views.success),
]


