# -*- coding:utf-8 -*-
from django.db import models
from django.core.urlresolvers import reverse

from django.contrib.auth.models import User

class Usermessage(models.Model):
    sender = models.ForeignKey(User, related_name="outbox", editable=False, verbose_name=u"От кого")
    recipient = models.ForeignKey(User, related_name="inbox", editable=False, verbose_name=u"Кому")
    
    subject = models.CharField(max_length=100, null=True, blank=True, verbose_name=u"Тема")
    text = models.TextField(verbose_name=u"Сообщение")
    
    is_draft = models.BooleanField(default=True, verbose_name=u"Черновик")
    
    is_read = models.BooleanField(default=False, verbose_name=u"Прочитано")
    
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)
    
    sender_deleted_at = models.DateTimeField(null=True, blank=True)
    sender_deleted_permanent = models.BooleanField(default=False)
    
    recipient_deleted_at = models.DateTimeField(null=True, blank=True)
    recipient_deleted_permanent = models.BooleanField(default=False)
    
    def __unicode__(self):
        if self.subject.strip() == "":
            return u"Без темы"
        return self.subject
    
    class Meta:
        verbose_name = u"Сообщение"
        verbose_name_plural = u"Сообщения"
    
    
    def get_absolute_url(self):
        return reverse('usermessages_message_show', args=[self.pk])
    

