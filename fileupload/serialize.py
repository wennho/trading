# encoding: utf-8
import mimetypes
import re
from django.core.urlresolvers import reverse


def order_name(name):
    """order_name -- Limit a text to 20 chars length, if necessary strips the
    middle of the text and substitute it for an ellipsis.

    name -- text to be limited.

    """
    name = re.sub(r'^.*/', '', name)
    if len(name) <= 20:
        return name
    return name[:10] + "..." + name[-7:]


def createJsonError(form_errors):
    error = []
    error_label = []
    for field, err in form_errors.items():
        error += err
        error_label += [field]

    return {
        'type': 'error',
        'error': error,
        'error_label': error_label,
    }


def serialize(instance, file_attr='file'):
    """serialize -- Serialize a Picture instance into a dict.

    instance -- Picture instance
    file_attr -- attribute name that contains the FileField or ImageField

    """
    return {
        'url': reverse('peerShop:item-detail', args=[instance.pk]),
        'thumbs': [{'url': pic.thumb.url,
                    'type': mimetypes.guess_type(pic.thumb.path)[0] or 'image/png',
                    'deleteUrl': reverse('itempic-delete', args=[pic.pk]),
                   } for pic in instance.itempic_set.all()],
        'deleteUrl':
            reverse('upload-delete', args=[instance.pk]),
        'updateUrl': reverse('upload-update', args=[instance.pk]),
        'deleteType': 'DELETE',
        'updateType': 'POST',
        'description': instance.description,
        'title': instance.title,
        'price': str(instance.price),
        'id': instance.pk,
    }


