from django.conf.urls.defaults import *

urlpatterns = patterns('welcome.views',
    (r'^$', 'index'),
)
