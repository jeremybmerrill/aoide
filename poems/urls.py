from django.conf.urls import patterns, url

from poems import views

urlpatterns = patterns('',
    # ex: /poems/
    url(r'^$', views.index, name='index'),

    # ex: /poems/5/
    url(r'^(?P<poem_id>\d+)/$', views.detail, name='detail'),

    # ex: /poems/5/vote/
    url(r'^(?P<poem_id>\d+)/vote/$', views.vote, name='vote'),

    # ex: /poems/5/create/ #heh, POST, eventually
    url(r'^(?P<poem_id>\d+)/create/$', views.create, name='create'),
)
