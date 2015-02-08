from django.conf.urls import patterns, include, url
from django.contrib import admin
from noodle import settings

urlpatterns = patterns('',
    (r'^media/(.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'products.views.index', name="index"),
    url(r'^create$', 'products.views.create'),
    url(r'^read/(?P<pk>\d+)/$', 'products.views.read'),
    url(r'^delete/(?P<pk>\d+)/$', 'products.views.delete'),
    url(r'^update$', 'products.views.update'),
    url(r'^get_list$', 'products.views.get_list'),
    url(r'^search$', 'products.views.search'),
)