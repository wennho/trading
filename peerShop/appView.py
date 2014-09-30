from django.views.generic import ListView
from fileupload.models import Item
from fileupload.response import JSONResponse, response_mimetype
from fileupload.views import ItemCreateView
from django.core.urlresolvers import reverse

def serialize(instance, file_attr='file'):
    """serialize -- Serialize a Picture instance into a dict.

    instance -- Picture instance
    file_attr -- attribute name that contains the FileField or ImageField

    """
    obj = instance.image

    return {
        'thumbnailUrl': instance.thumb.url,
        'deleteUrl': reverse('upload-delete', args=[instance.pk]),
        'updateUrl': reverse('upload-update', args=[instance.pk]),
        'id': instance.pk,
        'description': instance.description,
        'title': instance.title,
        'price': str(instance.price),
        'imageUrl': instance.image.url,
        'user': instance.user.username,
        'user_email': instance.user.email,
    }



class AppItemListView(ListView):
    model = Item

    def render_to_response(self, context, **response_kwargs):
        data = [serialize(p) for p in Item.objects.order_by('-edit_date')]
        return JSONResponse(data, mimetype=response_mimetype(self.request))

class AppItemCreateView(ItemCreateView):

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        data = [serialize(self.object)]
        return JSONResponse(data, mimetype=response_mimetype(self.request))