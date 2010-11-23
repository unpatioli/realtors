# -*- coding:utf-8 -*-
from django.db import models

from django.contrib.auth.models import User

class Usermessage(models.Model):
    sender = models.ForeignKey(User, related_name="outbox", verbose_name=u"От кого")
    recipient = models.ForeignKey(User, related_name="inbox", verbose_name=u"Кому")
    
    subject = models.CharField(max_length=100, null=True, blank=True, verbose_name=u"Тема")
    text = models.TextField(verbose_name=u"Сообщение")
    
    is_draft = models.BooleanField(default=True, verbose_name=u"Черновик")
    
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)
    deleted_at = models.DateTimeField(null=True, blank=True, verbose_name=u"Удалено")
    
    def __unicode__(self):
        if self.subject.strip() == "":
            return u"Без темы"
        return self.subject
    
    class Meta:
        verbose_name = u"Сообщение"
        verbose_name_plural = u"Сообщения"
