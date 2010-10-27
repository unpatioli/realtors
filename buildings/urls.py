from django.conf.urls.defaults import *

rent_flats_patterns = patterns('buildings.views',
    (r'^rent_flats$', 'rent_flats_list'),
    (r'^rent_flats/new$', 'rent_flats_new'),
    (r'^rent_flats/create$', 'rent_flats_create'),
    (r'^rent_flats/edit/(?P<id>\d+)', 'rent_flats_edit'),
    (r'^rent_flats/update/(?P<id>\d+)', 'rent_flats_update'),
    (r'^rent_flats/delete/(?P<id>\d+)', 'rent_flats_delete')
)

sell_flats_patterns = patterns('buildings.views',
    (r'^sell_flats$', 'sell_flats_list'),
    (r'^sell_flats/new$', 'sell_flats_new'),
    (r'^sell_flats/create$', 'sell_flats_create'),
    (r'^sell_flats/edit/(?P<id>\d+)', 'sell_flats_edit'),
    (r'^sell_flats/update/(?P<id>\d+)', 'sell_flats_update'),
    (r'^sell_flats/delete/(?P<id>\d+)', 'sell_flats_delete')
)

urlpatterns = 
    patterns('buildings.views', (r'^$', 'index')) +
    rent_flats_patterns +
    sell_flats_patterns