from django.conf.urls import patterns, url
from django.views.generic import TemplateView
from views import *
from community_views import *
from bidView import *
from linkView import *
from appView import *

urlpatterns = patterns('',
                       url(r'^$', MainView.as_view(), name='main'),
                       url(r'^faq/', TemplateView.as_view(template_name='peerShop/faq.html'), name='faq'),
                       url(r'^guide/', TemplateView.as_view(template_name='peerShop/guide.html'), name='guide'),
                       url(r'^contact/', TemplateView.as_view(template_name='peerShop/contact.html'), name='contact'),
                       url(r'^terms/', TemplateView.as_view(template_name='peerShop/terms.html'), name='terms'),
                       url(r'^community/(?P<pk>\d+)/$', CommunityDetailView.as_view(), name='community_detail'),
                       url(r'^user/(?P<username>\w+)/community/$', UserCommunityView.as_view(), name='user_community'),
                       url(r'^shop/(?P<username>\w+)/$', ShopView.as_view(), name='shop'),
                       url(r'^item/(?P<pk>\d+)/$', ItemDetailView.as_view(), name='item-detail'),
                       url(r'^bid/list/$', BidListView.as_view(), name='bid-list'),
                       url(r'^bid/update/(?P<pk>\d+)$', BidUpdateView.as_view(), name='bid-update'),
                       url(r'^bid/new/$', BidCreateView.as_view(), name='bid-new'),
                       url(r'^bid/delete/(?P<pk>\d+)$', BidDeleteView.as_view(), name='bid-delete'),
                       url(r'^link/new/$', CreateLink.as_view(), name='link_new'),
                       url(r'^link/(?P<username>[\w.@+-]+)/$', LinkedListView.as_view(), name='linked_list'),
                       url(r'^search$', SearchView.as_view(), name='item-search'),
                       url(r'^app/item/new/$', AppItemCreateView.as_view(), name='app-item-create'),
                       url(r'^app/item/$', AppItemListView.as_view(), name='app-item-all'),
)
