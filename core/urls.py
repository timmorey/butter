##
# urls.py - Created by Timothy Morey on 2/8/2014
#

from django.conf.urls import patterns, url

from core import views

idpattern = '[a-zA-Z0-9_-]+'

urlpatterns = patterns('',
    url(r'^dialect/$', 
        views.dialectroot),
    url(r'^dialect/(?P<dialectid>' + idpattern + ')/$', 
        views.dialectdetail),

    url(r'^index/$',
        views.indexroot),
    url(r'^index/(?P<indexid>' + idpattern + ')/$',
        views.indexdetail),

    url(r'^resource/$', 
        views.resourceroot),
    url(r'^resource/(?P<resourceid>' + idpattern + ')/$', 
        views.resourcedetail),

    url(r'^unit/$', 
        views.unitroot),
    url(r'^unit/(?P<unitid>' + idpattern + ')/$', 
        views.unitdetail),
)
