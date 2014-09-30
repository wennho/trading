"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from django.test.client import Client
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from models import Item, Bid
from mysite.settings import PROJECT_PATH


class TestPeerShop(TestCase):
    def setUp(self):
        user = User.objects.create_user('test', '', 'test')
        self.item = Item(
            user=user,
            image=PROJECT_PATH + '/test/IMG_0699.JPG',
            thumb=PROJECT_PATH + '/test/IMG_0699_thumbnail.JPG',
            title='keyboard',
            description='kkk',
            price=10
        )
        super(Item, self.item).save()
        user2 = User.objects.create_user('test2', '', 'test2')
        self.bid = Bid(
            bidUser=user2,
            bidPrice=10,
            itemUser=user,
            item=self.item,
            status='-'
        )
        self.bid.save()

    def test_views_integration(self):
        c = Client()

        response = c.get(reverse('peerShop:main'))
        assert response.status_code == 200
        assert 'PeerShop' in response.content

        response = c.get(reverse('peerShop:bid-list'))
        assert response.status_code == 200
        assert 'PeerShop' in response.content

        response = c.get(reverse('peerShop:shop', args=('test',)))
        assert response.status_code == 200
        assert 'PeerShop' in response.content

        response = c.get(reverse('peerShop:item-detail', args=(self.item.id,)))
        assert response.status_code == 200
        assert self.item.title in response.content


    def test_login_view(self):
        c = Client()
        assert c.login(username='test', password='test')

        response = c.get(reverse('peerShop:shop', args=('test',)))
        assert response.status_code == 200
        assert 'PeerShop' in response.content

    def test_bid_delete(self):
        c = Client()
        assert c.login(username='test2', password='test2')
        response = c.post(
            reverse('peerShop:bid-delete', args=(self.bid.id,)),
        )

        assert response.status_code == 200
        assert 'Deleted' in response.content, response.content
        assert not Bid.objects.filter(id=self.bid.id).exists()