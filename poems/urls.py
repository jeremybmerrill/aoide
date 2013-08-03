from django.conf.urls import patterns, url

from django.views import generic

from poems import views
from poems.models import Source


urlpatterns = patterns('',
    # ex: /poems/
    url(r'^$', views.index, name='index'),

    # ex: /poems/5/
    url(r'^(?P<poem_id>\d+)/$', views.detail, name='detail'),

    # ex: /poems/5/vote/
    url(r'^(?P<poem_id>\d+)/vote/$', views.snap, name='vote'),

    # # ex: /poems/create/
    # url(r'^new/$', views.new, name='new'),

    # ex: /poems/create/
    url(r'^create/$', views.create, name='create'),


    # url(r'^sources/$', generic.TemplateView.as_view(
    #     queryset=Source.objects.all()[:5],
    #     ), name="source_list", ),
    #url(r'^sources/(?P<source_id>\d+)/$', generic.ListView.as_view(), name="source_detail")

)
