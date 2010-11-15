# -*- coding:utf-8 -*-
from django.conf.urls.defaults import *
from django.conf import settings

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^realtors/', include('realtors.foo.urls')),
    (r'^$', include('welcome.urls')),
    
    (r'^accounts/', include('accounts.urls')),
    (r'^buildings/', include('buildings.urls')),
    
    # Django comments system
    (r'^comments/', include('django.contrib.comments.urls')),
    
    # Uncomment the admin/doc line below to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # (r'^admin/', include(admin.site.urls)),
)

# ¡¡¡ Only in dev mode !!!
if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^{staticfiles_url}(?P<path>.*)$'.format(staticfiles_url=settings.STATICFILES_URL[1:]),
            'django.views.static.serve',
            {'document_root': settings.STATICFILES_DOC_ROOT}),
    )
    
    media_url = settings.MEDIA_URL
    if media_url[0] == '/':
        media_url = media_url[1:]
    urlpatterns += patterns('',
        (r'^{media_url}(?P<path>.*)$'.format(media_url=media_url),
            'django.views.static.serve',
            {'document_root': settings.MEDIA_ROOT}),
    )

