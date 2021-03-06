from django.conf.urls import patterns, include, url
from django.contrib import admin

import views

urlpatterns = patterns('',
	# Things every user will see
    url(r'^$', 'competition.views.home', name='home'),
    url(r'^updates/$', 'competition.views.updates', name='updates'),
    url(r'^info/$', 'competition.views.info', name='info'),
    
    # User management URLs
    url(r'^signin/$', 'competition.views.signin', name='signin'),
    url(r'^create/$', 'competition.views.createaccount', name='createaccount'),
    url(r'^delete/$', 'competition.views.auth_delete', name='delete'),
    url(r'^logout/$', 'competition.views.auth_logout', name='logout'),
    url(r'^password/$', 'competition.views.resetpassword', name='password'),
    url(r'^newpassword/$', 'competition.views.newpassword', name='newpassword'),
    
    # Admin-specific things
    url(r'^participants/$', 'competition.views.participants', name='participants'),
    url(r'^createupdate/$', 'competition.views.createupdate', name='createupdate'),
)
