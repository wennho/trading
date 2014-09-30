from django.forms import ModelForm
from django.views.generic import CreateView
from django.contrib.auth.models import User
from django.http.response import HttpResponseRedirect

from views import UserBasedListView
from models import Link


class LinkedListView(UserBasedListView):
    model = User
    template_name = 'peerShop/link_list.html'

    def get_context_data(self, user, **kwargs):

        mutual = User.objects.filter(linkFrom__toUser=user, linkTo__fromUser=user)
        to_add_back = user.linkTo.all().exclude(fromUser__in=mutual)

        kwargs.update({
            'to_add_back': to_add_back,
            'mutual': mutual,
            'profile_user': user,
            'activePeers': True,
        })
        context = super(UserBasedListView, self).get_context_data(**kwargs)
        return context

class CreateLinkForm(ModelForm):
    class Meta:
        model = Link
        exclude = ('fromUser',)

class CreateLink(CreateView):
    model = Link
    form_class = CreateLinkForm
    template_name = 'peerShop/bid.html' # filler

    def form_valid(self, form):
        link = form.save(commit=False)
        link.fromUser = self.request.user
        link.save()
        return HttpResponseRedirect(form.data['next'])

    def get_success_url(self):
        """
        Returns the supplied success URL.
        """
        return self.request.path

