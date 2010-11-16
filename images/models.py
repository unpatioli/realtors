# -*- coding:utf-8 -*-
from django.db import models
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic

from image_utils.modelfields import ResizedImageField

class ImagedItem(models.Model):
    title = models.CharField(max_length=100, default=u"Без названия", verbose_name=u"Подпись")
    image = ResizedImageField(upload_to='item_images', dimensions=settings.PHOTO_SIZE, verbose_name=u"Фото")
    thumbnail = ResizedImageField(upload_to='item_thumbnails', dimensions=settings.THUMBNAIL_SIZE)
    
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)
    deleted_at = models.DateTimeField(null=True, blank=True, editable=False)
    
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey('content_type', 'object_id')
    
    def save(self, *args, **kwargs):
        if self.pk is not None:
            orig = ImagedItem.objects.get(pk=self.pk)
            if orig.image != self.image:
                name = self.image.name.rsplit('.',1)[0]
                self._meta.get_field('thumbnail').save_form_data(self, self.image.file, name=name)
        else:
            name = self.image.name.rsplit('.',1)[0]
            self._meta.get_field('thumbnail').save_form_data(self, self.image.file, name=name)
        super(ImagedItem, self).save(*args, **kwargs)
    
    def __unicode__(self):
        return self.title
    

