from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^core/', include('butter.core.urls')),
    url(r'^authentication/', include('butter.authentication.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
