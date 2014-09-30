# encoding: utf-8
from django.conf.urls import patterns, url
from fileupload.views import *

urlpatterns = patterns('',
    url(r'^new/$', ItemCreateView.as_view(), name='upload-new'),
    url(r'^delete/(?P<pk>\d+)$', ItemDeleteView.as_view(), name='upload-delete'),
    url(r'^view/$', ItemListView.as_view(), name='upload-view'),
    url(r'^update/(?P<pk>\d+)$', ItemUpdateView.as_view(), name='upload-update'),
    url(r'^itempic/new/$', ItemPicCreateView.as_view(), name='itempic-new'),
    url(r'^itempic/delete/(?P<pk>\d+)$', ItemPicDeleteView.as_view(), name='itempic-delete'),
)
