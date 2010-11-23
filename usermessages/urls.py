from django.conf.urls.defaults import *

urlpatterns = patterns('usermessages.views',
    url(    r'inbox/$',
            'inbox',
            name = 'usermessages_inbox'
    ),
    url(    r'outbox/$',
            'outbox',
            name = 'usermessages_outbox'
    ),
    url(    r'drafts/$',
            'drafts',
            name = 'usermessages_drafts'
    ),
    url(    r'trash/$',
            'trash',
            name = 'usermessages_trash'
    ),
    
    url(    r'new/to/(?P<user_id>\d+)/$',
            'message_new',
            name = 'usermessages_message_new'
    ),
    url(    r'(?P<object_id>\d+)/send/$',
            'message_send',
            name = 'usermessages_message_send'
    ),
    
    url(    r'(?P<object_id>\d+)/$',
            'message_show',
            name = 'usermessages_message_show'
    ),
    url(    r'(?P<object_id>\d+)/edit$',
            'message_edit',
            name = 'usermessages_message_edit'
    ),
    url(    r'(?P<object_id>\d+)/delete$',
            'message_delete',
            name = 'usermessages_message_delete'
    ),
)
