from django.conf.urls import patterns, url

from poems import views

urlpatterns = patterns('',
    # ex: /poems/
    url(r'^$', views.index, name='index'),

    # ex: /poems/5/
    url(r'^(?P<poem_id>\d+)/$', views.detail, name='detail'),

    # ex: /poems/5/vote/
    url(r'^(?P<poem_id>\d+)/vote/$', views.snap, name='vote'),

    # ex: /poems/create/ #heh, POST, eventually
    url(r'^new/$', views.new, name='new'),

    # ex: /poems/create/ #heh, POST, eventually
    url(r'^create/$', views.create, name='create'),
)
