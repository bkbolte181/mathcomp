from django.conf.urls import patterns, include, url
from django.contrib import admin

import views

urlpatterns = patterns('',
    url(r'^$', 'mathcomp.views.home', name='home'),
    url(r'^competition/', include('competition.urls', namespace='competition')),
    
    url(r'^admin/', include(admin.site.urls)),
)
