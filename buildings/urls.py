from django.conf.urls.defaults import *

urlpatterns = patterns('buildings.views',
    (r'^$', 'index'),
    (r'^rent_flats/$', 'rent_flats_list'),
    
)