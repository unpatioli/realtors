# -*- coding:utf-8 -*-
from django.conf.urls.defaults import patterns, include, url
from django.conf import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^realtors/', include('realtors.foo.urls')),
    (r'^$', include('welcome.urls')),
    
    (r'^accounts/', include('accounts.urls')),
    (r'^buildings/', include('buildings.urls')),
    
    (r'^images/', include('images.urls')),
    (r'^messages/', include('usermessages.urls')),
    # Django comments system
    (r'^comments/', include('django.contrib.comments.urls')),
    
    # Uncomment the admin/doc line below to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
)

# ¡¡¡ Only in dev mode !!!
if settings.SERVE_STATIC:
    urlpatterns += patterns('django.contrib.staticfiles.views',
        url(r'^static/(?P<path>.*)$', 'serve'),
    )
    
    media_url = settings.MEDIA_URL
    if media_url[0] == '/':
        media_url = media_url[1:]
    urlpatterns += patterns('',
        (r'^%(media_url)s(?P<path>.*)$' % {'media_url': media_url},
            'django.views.static.serve',
            {'document_root': settings.MEDIA_ROOT}),
    )

