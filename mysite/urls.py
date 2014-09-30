from django.conf.urls import patterns, include, url
from settings import DEBUG, MEDIA_ROOT

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'mysite.views.home', name='home'),
    # url(r'^mysite/', include('mysite.foo.urls')),
    url(r'^', include('peerShop.urls', namespace="peerShop")),
    url(r'^user/', include('allauth.urls')),
    url(r'^upload/', include('fileupload.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)

if DEBUG:
    urlpatterns += patterns('', url(r'^media/(.*)$', 'django.views.static.serve', kwargs={'document_root': MEDIA_ROOT}), )