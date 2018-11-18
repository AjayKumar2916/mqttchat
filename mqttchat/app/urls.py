from django.conf.urls import url

from app.views import *

urlpatterns = [
    url(r'^$', login, name="login"),
    url(r'^dashboard/$', dashboard, name="dashboard"),
    url(r'^logout/$', logout, name="logout"),
    url(r'^message/(?P<topic_id>\d+)/$', message, name="message"),
    url(r'^publish/$', publish, name="publish"),
]