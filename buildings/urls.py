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
    url(    r'user/(?P<user_id>\d+)/objects/$',
            'user_object_list',
            name = 'buildings_user_object_list'
    ),
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
    url(    r'(?P<location>%s)/(?P<object_type>%s)/(?P<id>\d+)/delete/$' % (location_regexp, object_type_regexp),
            'object_delete',
            name = 'buildings_object_delete'
    ),
)

search_patterns = patterns('buildings.views',
    url(    r'search/$',
            'object_search',
            name = 'buildings_object_search'
    ),
    url(    r'search/(?P<location>%s)/(?P<object_type>%s)/$' % (location_regexp, object_type_regexp),
            'object_search',
            name = 'buildings_object_search'
    ),
)

urlpatterns = common_patterns + object_patterns + search_patterns