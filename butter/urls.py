from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^core/', include('core.urls')),
    url(r'^auth/', include('auth.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
