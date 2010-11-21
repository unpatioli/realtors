# -*- coding:utf-8 -*-
from django.db import models

class Currency(models.Model):
    title = models.CharField(max_length = 50, verbose_name=u"Название")
    char_id = models.CharField(max_length = 3, verbose_name=u"Буквенное обозначение")
    symbol = models.CharField(max_length = 1, verbose_name=u"Символ")
    
    def __unicode__(self):
        return self.symbol
    
    class Meta:
        verbose_name = u"Валюта"
        verbose_name_plural = u"Валюты"
    

