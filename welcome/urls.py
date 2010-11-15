from django.conf.urls.defaults import *

urlpatterns = patterns('welcome.views',
    url(r'^$', 'index', name='index'),
)
