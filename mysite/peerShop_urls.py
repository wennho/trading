from urls import urlpatterns
from django.conf.urls import patterns, include, url

# change urlconf so that peershop is at the root
urlpatterns = patterns('', url(r'^', include('peerShop.urls', namespace="peerShop")), ) + urlpatterns

