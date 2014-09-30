from django.views.generic import DetailView
from django.contrib.auth.models import Group

from views import UserBasedListView
from models import Community

class UserCommunityView(UserBasedListView):
    model = Community
    template_name = 'peerShop/user_community_view.html'

    def get_queryset(self, user):
        return user.groups.values

    def get_context_data(self, user, **kwargs):
        kwargs.update({
            'activeCommunity': True,
        })
        return super(UserBasedListView, self).get_context_data(**kwargs)

class CommunityDetailView(DetailView):
    model = Group
    template_name = 'peerShop/community_detail.html'

    def get_context_data(self, **kwargs):
        kwargs.update({
            'numPeers': len(self.object.user_set.all()),
            'activeCommunity': True,
        })
        return super(CommunityDetailView,self).get_context_data(**kwargs)