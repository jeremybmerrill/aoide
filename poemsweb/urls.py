from django.conf.urls import patterns, include, url
from django.conf import settings
from django.views.generic import TemplateView


# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'poemsweb.views.home', name='home'),
    # url(r'^poemsweb/', include('poemsweb.foo.urls')),

    url(r'^$', include('poems.urls')),
    url(r'^poems/', include('poems.urls', namespace="poems")),
    #url(r'^accounts/login/$', 'django.contrib.auth.views.login', name="login" ),
    #url(r'^accounts/logout/$', 'django.contrib.auth.views.logout', {'next_page': '/poems/'}, name="logout",),
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^about/', TemplateView.as_view(template_name="poems/about.html"), name="about"),
)

if settings.DEBUG:
  urlpatterns += patterns('',
       (r'^static/(?P<path>.*)$', 'django.views.static.serve',         
      {'document_root': settings.STATIC_ROOT, 'show_indexes': True})
  )
