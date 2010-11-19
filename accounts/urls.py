from django.conf.urls.defaults import *

urlpatterns = patterns('',
    url(    r'login/$', 
            'django.contrib.auth.views.login',
            {'template_name': 'accounts/login.html'},
            name = 'accounts_login'
    ),
    url(    r'logout/$',
            'django.contrib.auth.views.logout',
            {'template_name': 'accounts/logged_out.html'},
            name = 'accounts_logout'
    ),
    url(    r'register/$',
            'accounts.views.register',
            name = 'accounts_register'
    ),
    url(    r'account/$',
            'accounts.views.account_edit',
            name = 'accounts_account_edit'
    ),
    url(    r'password_change/$',
            'accounts.views.password_change',
            name = 'accounts_password_change'
    ),
    
    url(    r'profile/(?P<user_id>\d+)/$',
            'accounts.views.profile',
            name = 'accounts_profile'
    ),
    url(    r'profile/$',
            'accounts.views.my_profile',
            name = 'accounts_my_profile'
    ),
    url(    r'profile/new/$',
            'accounts.views.my_profile_new',
            name = 'accounts_my_profile_new'
    ),
    url(    r'profile/edit/$',
            'accounts.views.my_profile_edit',
            name = 'accounts_my_profile_edit'
    ),
    
    url(    r'profile/realtor/(?P<user_id>\d+)/$',
            'accounts.views.profile_realtor',
            name = 'accounts_profile_realtor'
    ),
    url(    r'profile/realtor/$',
            'accounts.views.my_profile_realtor',
            name = 'accounts_my_profile_realtor'
    ),
    url(    r'profile/realtor/new/$',
            'accounts.views.realtor_new',
            name = 'accounts_my_profile_realtor_new'
    ),
    url(    r'profile/realtor/edit/$',
            'accounts.views.realtor_edit',
            name = 'accounts_my_profile_realtor_edit'
    ),
    
    url(    r'agency/list/$',
            'accounts.views.agency_list',
            name = 'accounts_agency_list'
    ),
    url(    r'agency/(?P<object_id>\d+)/$',
            'accounts.views.agency_detail',
            name = 'accounts_agency_detail'
    ),
    url(    r'agency/new/$',
            'accounts.views.agency_new',
            name = 'accounts_agency_new'
    ),
    url(    r'agency/(?P<object_id>\d+)/edit/$',
            'accounts.views.agency_edit',
            name = 'accounts_agency_edit'
    ),
    url(    r'agency/(?P<object_id>\d+)/delete/$',
            'accounts.views.agency_delete',
            name = 'accounts_agency_delete'
    ),
    
)