from django.test import TestCase
from django.test.client import Client
from django.core.urlresolvers import reverse

class TestPostmanMod(TestCase):

    def test_views(self):

        c = Client()
        response = c.get(reverse('upload-new'))
        assert response.status_code == 200
        assert 'PeerShop' in response.content
