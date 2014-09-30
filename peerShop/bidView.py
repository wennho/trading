from django.forms import ModelForm
from django.views.generic import CreateView, TemplateView, DeleteView, UpdateView
from django.shortcuts import render
from django.http import HttpResponseForbidden, HttpResponseBadRequest
from .models import Bid


class CreateBidForm(ModelForm):
    class Meta:
        model = Bid
        exclude = ('bidUser', 'itemUser',)


class BidCreateView(CreateView):
    model = Bid
    form_class = CreateBidForm
    template_name = 'peerShop/bid.html'

    def form_valid(self, form):
        bid = form.save(commit=False)
        bid.bidUser = self.request.user
        bid.itemUser = bid.item.user
        bid.status = '-'
        bid.save()
        return render(self.request, 'peerShop/bid.html', {'bid': bid})


class BidUpdateView(UpdateView):
    model = Bid
    form_class = CreateBidForm
    # template_name = 'peerShop/bid.html'


    def form_valid(self, form):

        newbid = form.save(commit=False)
        origBid = Bid.objects.get(id=newbid.id)

        if self.request.user == origBid.bidUser and origBid.status == '-':
            origBid.bidPrice = newbid.bidPrice

        if self.request.user == origBid.itemUser and origBid.bidPrice == newbid.bidPrice:
            origBid.status = newbid.status

        origBid.save()

        return render(self.request, 'peerShop/bid.html', {'bid': origBid})

    def form_invalid(self, form):
        print form.errors
        return HttpResponseBadRequest()


class BidDeleteView(DeleteView):
    model = Bid

    def delete(self, request, *args, **kwargs):
        bid = self.get_object()
        if self.request.user == bid.bidUser:
            item = bid.item
            bid.delete()
            return render(
                self.request,
                'peerShop/bid.html',
                {'info': "<p class='deleted_item'>Deleted bid</p>", 'item': item})
        else:
            return HttpResponseForbidden("Only the bidding user can delete the bid.")


class BidListView(TemplateView):
    template_name = 'peerShop/bid_list.html'

    def get_context_data(self, **kwargs):
        context = super(BidListView, self).get_context_data(**kwargs)
        if self.request.user.is_authenticated():
            context['placedBids'] = self.request.user.placedBids.all()
            context['receivedBids'] = self.request.user.receivedBids.all()
            context['activeBid'] = True
        return context