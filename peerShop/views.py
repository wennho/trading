from django.views.generic import ListView, DetailView
from django.http import Http404
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django import forms
from search import get_query
from fileupload.models import Item
from models import Bid, Link


class UserBasedListView(ListView):
    def get_queryset(self, user):
        return None

    def get_context_data(self, user, **kwargs):
        return super(UserBasedListView, self).get_context_data(**kwargs)

    def get(self, request, *args, **kwargs):
        if 'username' in kwargs:
            username = kwargs['username']
            try:
                user = User.objects.get(username=username)
            except ObjectDoesNotExist:
                raise Http404
        elif self.request.user.is_authenticated():
            user = self.request.user
        else:
            # Cannot identify the user we are supposed to display the shop for.
            # Return to sign-in page
            return redirect('account_login')

        self.object_list = self.get_queryset(user)
        allow_empty = self.get_allow_empty()

        if not allow_empty:
            # When pagination is enabled and object_list is a queryset,
            # it's better to do a cheap query than to load the unpaginated
            # queryset in memory.
            if (self.get_paginate_by(self.object_list) is not None
                and hasattr(self.object_list, 'exists')):
                is_empty = not self.object_list.exists()
            else:
                is_empty = len(self.object_list) == 0
            if is_empty:
                raise Http404(_("Empty list and '%(class_name)s.allow_empty' is False.")
                              % {'class_name': self.__class__.__name__})
        context = self.get_context_data(user, object_list=self.object_list)
        return self.render_to_response(context)


def appendUserBid(bidUser, itemSet):
    if itemSet and bidUser.is_authenticated():
        itemSet = set(itemSet)
        bids = bidUser.placedBids.filter(item__in=itemSet)
        for bid in bids:
            itemSet.remove(bid.item)
            bid.item.bid = bid
            itemSet.add(bid.item)
    return itemSet


class ShopView(UserBasedListView):
    model = Item
    template_name = 'peerShop/shop.html'

    def get_queryset(self, user):
        itemSet = user.item_set.order_by('-edit_date')
        return appendUserBid(self.request.user, itemSet)

    def get_context_data(self, user, **kwargs):
        kwargs.update({
            'shopuser': user,
            'networks': ', '.join(user.groups.values_list('name', flat=True)),
            'activeShop': True,
            'numPeers': user.linkTo.count(),
        })

        if self.request.user.is_authenticated():
            kwargs['isLinked'] = Link.objects.filter(fromUser=self.request.user.id, toUser=user).exists()
        return super(UserBasedListView, self).get_context_data(**kwargs)


class ItemDetailView(DetailView):
    model = Item
    template_name = 'peerShop/item_detail.html'

    def get_context_data(self, **kwargs):
        context = super(ItemDetailView, self).get_context_data(**kwargs)
        if self.request.user.is_authenticated():
            context['bid'] = Bid.objects.filter(bidUser=self.request.user.id, item=self.object).first()
        return context


class MainView(ListView):
    model = Item
    template_name = 'peerShop/main.html'

    def get_queryset(self):
        itemSet = Item.objects.order_by('-edit_date')[:30]
        return appendUserBid(self.request.user, itemSet)


class SearchView(ListView):
    model = Item
    template_name = 'peerShop/search.html'

    def search(self, request):
        found_entries = None
        if ('q' in request.GET) and request.GET['q'].strip():
            query_string = request.GET['q']
            entry_query = get_query(query_string, ['title'])
            found_entries = Item.objects.filter(entry_query).order_by('-edit_date')
            if 'maxPrice' in request.GET and request.GET['maxPrice']:
                try:
                    maxPrice = float(request.GET['maxPrice'])
                    found_entries = found_entries.filter(price__lte=maxPrice)
                except ValueError:
                    found_entries = None
        return found_entries

    def get_queryset(self):
        itemSet = self.search(self.request)
        return appendUserBid(self.request.user, itemSet)