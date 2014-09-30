# encoding: utf-8
from django.db import models
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from PIL import Image
from cStringIO import StringIO
import os


def upload_to(instance, filename):
    return 'user/%s/%s' % (instance.item.user.username, filename)


def fit_crop(img, max_width=None, max_height=None):
    # Store original image width and height
    w, h = float(img.size[0]), float(img.size[1])

    # Use the original size if no size given
    max_width = float(max_width or w)
    max_height = float(max_height or h)

    # Find the closest bigger proportion to the maximum size
    scale = max(max_width / w, max_height / h)

    # Image bigger than maximum size?
    if (scale < 1):
        # Calculate proportions and resize
        w = int(w * scale)
        h = int(h * scale)
        img = img.resize((w, h), Image.ANTIALIAS)
        img.load()


    # Avoid enlarging the image
    max_width = min(max_width, w)
    max_height = min(max_height, h)

    # Define the cropping box
    left = int((w - max_width) / 2)
    top = int((h - max_height) / 2)
    right = int(left + max_width)
    bottom = int(top + max_height)

    # Crop to fit the desired size
    img = img.crop((left, top, right, bottom))
    img.load()
    return img


class Item(models.Model):
    user = models.ForeignKey(User)
    title = models.CharField(max_length=140)
    description = models.TextField(max_length=500, blank=True)
    price = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    edit_date = models.DateField(auto_now=True)

    def __unicode__(self):
        return self.title

    @models.permalink
    def get_absolute_url(self):
        return ('upload-new', )

class ItemPic(models.Model):
    """This is a small demo using just two fields. The slug field is really not
    necessary, but makes the code simpler. ImageField depends on PIL or
    pillow (where Pillow is easily installable in a virtualenv. If you have
    problems installing pillow, use a more generic FileField instead.
    """
    image = models.ImageField(upload_to=upload_to)
    thumb = models.ImageField(upload_to=upload_to, default='')
    item = models.ForeignKey(Item)

    def __unicode__(self):
        return self.image.name

    def save(self, *args, **kwargs):
        self.create_thumbnail()
        super(ItemPic, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        """delete -- Remove to leave file."""
        self.image.delete(False)
        self.thumb.delete(False)
        super(ItemPic, self).delete(*args, **kwargs)

    def update(self, *args, **kwargs):
        super(ItemPic, self).save(*args, **kwargs)


    def create_thumbnail(self):
        # original code for this method came from
        # http://snipt.net/danfreak/generate-thumbnails-in-django-with-pil/

        # If there is no image associated with this.
        # do not create thumbnail
        if not self.image:
            return

        DJANGO_TYPE = self.image.file.content_type

        if DJANGO_TYPE == 'image/jpeg':
            PIL_TYPE = 'jpeg'
            FILE_EXTENSION = 'jpg'
        elif DJANGO_TYPE == 'image/png':
            PIL_TYPE = 'png'
            FILE_EXTENSION = 'png'

        # Open original photo which we want to thumbnail using PIL's Image
        image = Image.open(StringIO(self.image.read()))

        # We use our PIL Image object to create the thumbnail
        im = fit_crop(image, 400, 400)
        image.im = im.im
        image.mode = im.mode
        image.size = im.size
        image.readonly = 0

        # Save the thumbnail
        temp_handle = StringIO()
        image.save(temp_handle, PIL_TYPE)
        temp_handle.seek(0)

        # Save image to a SimpleUploadedFile which can be saved into
        # ImageField
        suf = SimpleUploadedFile(os.path.split(self.image.name)[-1],
                                 temp_handle.read(), content_type=DJANGO_TYPE)
        # Save SimpleUploadedFile into image field
        self.thumb.save('%s_thumbnail.%s' % (os.path.splitext(suf.name)[0], FILE_EXTENSION), suf, save=False)
