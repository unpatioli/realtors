from django.conf.urls.defaults import *

rent_flats_patterns = patterns('buildings.views',
    (r'^rent/flats$', 'rent_flats_list'),
    (r'^rent/flats/new$', 'rent_flats_new'),
    (r'^rent/flats/create$', 'rent_flats_create'),
    (r'^rent/flats/edit/(?P<id>\d+)', 'rent_flats_edit'),
    (r'^rent/flats/update/(?P<id>\d+)', 'rent_flats_update'),
    (r'^rent/flats/delete/(?P<id>\d+)', 'rent_flats_delete')
)

sell_flats_patterns = patterns('buildings.views',
    (r'^sell/flats$', 'sell_flats_list'),
    (r'^sell/flats/new$', 'sell_flats_new'),
    (r'^sell/flats/create$', 'sell_flats_create'),
    (r'^sell/flats/edit/(?P<id>\d+)', 'sell_flats_edit'),
    (r'^sell/flats/update/(?P<id>\d+)', 'sell_flats_update'),
    (r'^sell/flats/delete/(?P<id>\d+)', 'sell_flats_delete')
)

urlpatterns = patterns('buildings.views', (r'^$', 'index')) + \
    rent_flats_patterns + \
    sell_flats_patterns