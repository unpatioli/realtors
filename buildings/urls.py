from django.conf.urls.defaults import *

from buildings.location_dispatcher import LOCATION_FORMS, LocationDispatcher

common_patterns = patterns('buildings.views',
    # (r'/$', 'index'),
    # (r'user/(?P<user_id>\d+)/$', 'user_index'),
)

location_regexp = r"\b%s\b" % r"\b|\b".join([location for location in LOCATION_FORMS])
deal_type_regexp = r"\b%s\b" % r"\b|\b".join([deal_type[0] for deal_type in LocationDispatcher.deal_types()])
object_type_regexp = r"\b%s\b" % r"\b|\b".join([object_type[0] for object_type in LocationDispatcher.object_types()])

object_patterns = patterns('buildings.views',
    url(    r'user/(?P<user_id>\d+)/(?P<location>%s)/(?P<object_type>%s)/$' % (location_regexp, object_type_regexp),
            'user_object_list',
            name = 'buildings_user_object_list'
    ),
    url(    r'(?P<location>%s)/(?P<object_type>%s)/(?P<id>\d+)/$' % (location_regexp, object_type_regexp),
            'object_detail',
            name = 'buildings_object_detail'
    ),
    url(    r'(?P<location>%s)/(?P<object_type>%s)/new/$' % (location_regexp, object_type_regexp),
            'object_new',
            name = 'buildings_object_new'
    ),
    url(    r'(?P<location>%s)/(?P<object_type>%s)/(?P<id>\d+)/edit/$' % (location_regexp, object_type_regexp),
            'object_edit',
            name = 'buildings_object_edit'
    ),
)

search_patterns = patterns('buildings.views',
    url(    r'search/rent/flat/moscow/$',
            'moscow_rentflat_search',
            name = 'buildings_moscow_rentflat_search'
    ),
    url(    r'search/rent/flat/moscow_region/$',
            'moscow_region_rentflat_search',
            name = 'buildings_moscow_region_rentflat_search'
    ),
    url(    r'search/rent/flat/common/$',
            'common_rentflat_search',
            'buildings_common_rentflat_search'
    ),
    
    url(    r'search/sell/flat/moscow/$',
            'moscow_sellflat_search',
            'buildings_moscow_sellflat_search'
    ),
    url(    r'search/sell/flat/moscow_region/$',
            'moscow_region_sellflat_search',
            'buildings_moscow_region_sellflat_search'
    ),
    url(    r'search/sell/flat/common/$',
            'common_sellflat_search',
            'buildings_common_sellflat_search'
    ),
)

urlpatterns = common_patterns + object_patterns + search_patterns