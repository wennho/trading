# encoding: utf-8
from django.views.generic import CreateView, DeleteView, ListView, UpdateView
from django.shortcuts import render_to_response, HttpResponse
from .models import Item, ItemPic
from .response import JSONResponse, response_mimetype
from .serialize import serialize, createJsonError
from django.forms import ModelForm
from django.core.context_processors import csrf
from django.core.urlresolvers import reverse


class CreateItemForm(ModelForm):
    class Meta:
        model = Item
        exclude = ('user', 'thumb',)


# TODO: fix this. item creation done somewhere else.
class ItemCreateView(CreateView):
    model = Item
    form_class = CreateItemForm

    def get_form_kwargs(self):
        kwargs = {'initial': self.get_initial()}
        if self.request.method in ('POST', 'PUT'):
            kwargs.update({
                'data': self.request.POST,
                'files': self.request.FILES,
            })

            # hack to make sure the right data is assigned. this is done in templatetags/upload_tags.py
            # TODO: change file-upload.js to only send the right data
            prefix = kwargs['files']['file'].name
            kwargs['files']['image'] = kwargs['files']['file']
            kwargs['data']['title'] = kwargs['data'][prefix + '-title']
            price = kwargs['data'][prefix + '-price'].strip(' $')
            kwargs['data']['price'] = price
            kwargs['data']['description'] = kwargs['data'][prefix + '-description']
        return kwargs

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        files = [serialize(self.object)]
        data = {'files': files}
        return render_to_response('fileupload/item_view_list.html', data)


    # TODO: fix error handling
    def form_invalid(self, form):
        files = [createJsonError(form.errors)]
        data = {'files': files}
        response = JSONResponse(data, mimetype=response_mimetype(self.request))
        response['Content-Disposition'] = 'inline; filename=files.json'
        return response

    def get_context_data(self, **kwargs):
        context = super(ItemCreateView, self).get_context_data(**kwargs)
        context['activeNew'] = True
        return context


class CreateItemPicForm(ModelForm):
    class Meta:
        model = ItemPic
        exclude = ('thumb',)


class ItemPicCreateView(CreateView):
    model = ItemPic
    form_class = CreateItemPicForm
    template_name = 'generic/form.html'

    def form_valid(self, form):
        """
        Just return the thumbnail url
        """
        item_pic = form.save()
        data = {
            'itemUrl': reverse('peerShop:item-detail', args=[item_pic.item.pk]),
            'item': item_pic.item,
            'thumb': item_pic.thumb,
            'deleteThumbUrl': reverse('itempic-delete', args=[item_pic.pk]),
        }
        return render_to_response('fileupload/itempic_preview.html', data)


class ItemPicDeleteView(DeleteView):
    model = ItemPic

    def delete(self, request, *args, **kwargs):
        self.get_object().delete()
        return HttpResponse("")


# TODO: only allow correct user to delete/update items
class ItemDeleteView(DeleteView):
    model = Item

    def delete(self, request, *args, **kwargs):
        self.get_object().delete()
        return HttpResponse("")


class ItemUpdateView(UpdateView):
    model = Item
    form_class = CreateItemForm
    template_name = 'fileupload/update.html'

    def form_valid(self, form):
        """
        If the form is valid, save the associated model.
        """
        self.object = form.save(commit=False)
        self.object.update()
        files = [serialize(self.object)]
        data = {'files': files}
        return render_to_response('fileupload/item_view_list.html', data)


class ItemListView(ListView):
    model = Item

    def render_to_response(self, context, **response_kwargs):
        files = [serialize(p) for p in self.request.user.item_set.order_by('-edit_date')]
        data = {'files': files}
        data.update(csrf(self.request))
        data['createItemPicUrl'] = reverse('itempic-new')
        return render_to_response('fileupload/item_view_list.html', data)
