##
# urls.py - Created by Timothy Morey on 2/17/2014
#

from django.conf.urls.defaults import patterns, url

from auth import views

urlpatterns = patterns('',
    url(r'^login/$', views.login),
    url(r'^logout/$', views.logout),
)
