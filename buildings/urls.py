from django.conf.urls.defaults import *

common_patterns = patterns('buildings.views',
    # (r'/$', 'index'),
    # (r'user/(?P<user_id>\d+)/$', 'user_index'),
)

rentflat_patterns = patterns('buildings.views',
    (r'user/(?P<user_id>\d+)/rent/flats/$', 'user_rentflat_list'),
    (r'rent/flats/(?P<id>\d+)/$', 'rentflat_detail'),
    (r'rent/flats/new/(?P<location>\w+)/$', 'rentflat_new'),
    (r'rent/flats/(?P<id>\d+)/edit/$', 'rentflat_edit'),
    # (r'rent/flats/(?P<id>\d+)/delete/$', 'rentflat_delete')
)

sellflat_patterns = patterns('buildings.views',
    # (r'(?P<user_id>\d+)/sell/flats/user/$', 'user_sellflat_list'),
    # (r'sell/flats/(?P<id>\d+)/$', 'sellflat_detail'),
    # (r'sell/flats/new/$', 'sellflat_new'),
    # (r'sell/flats/(?P<id>\d+)/edit/$', 'sellflat_edit'),
    # (r'sell/flats/(?P<id>\d+)/delete/$', 'sellflat_delete')
)

urlpatterns = common_patterns + rentflat_patterns + sellflat_patterns