# -*- coding:utf-8 -*-
from django.db import models

def get_rate_from_service(curr):
    from decimal import Decimal
    
    if curr == 'EUR':
        return Decimal(1)
    
    import urllib2
    from lxml import etree
    
    web_service_url = "http://www.ecb.europa.eu/stats/eurofxref/eurofxref-daily.xml"
    namespaces = {
        'ns1': "http://www.gesmes.org/xml/2002-08-01",
        'ns2': "http://www.ecb.int/vocabulary/2002-08-01/eurofxref"
    }
    xpath_expr = "//ns1:Envelope/ns2:Cube/ns2:Cube[last()]/ns2:Cube[@currency='%s'][@rate]"
    
    tree = etree.parse(urllib2.urlopen(web_service_url))
    curr1_expr = xpath_expr % curr
    el = tree.xpath(curr1_expr, namespaces = namespaces)
    if not len(el):
        raise Exception("No rate found")
    return Decimal(el[0].get('rate'))

def get_rate(curr):
    if curr == 'EUR':
        from decimal import Decimal
        return Decimal(1)
    
    from django.core.cache import cache
    currency_rates_dict = cache.get('currency_rates_dict', {})
    if curr in currency_rates_dict:
        return currency_rates_dict[curr]
    rate = get_rate_from_service(curr)
    currency_rates_dict[curr] = rate
    cache.set('currency_rates_dict', currency_rates_dict, 60*60*24)
    return rate
    

# Managers
class ActiveManager(models.Manager):
    def get_query_set(self):
        return super(ActiveManager, self).get_query_set()
    

# Model
class Currency(models.Model):
    title = models.CharField(max_length = 50, verbose_name=u"Название")
    char_id = models.CharField(max_length = 3, verbose_name=u"Буквенное обозначение")
    symbol = models.CharField(max_length = 4, verbose_name=u"Символ")
    
    def __unicode__(self):
        return self.symbol
    
    @property
    def rate(self):
        return get_rate(self.char_id)
    
    # ============
    # = Managers =
    # ============
    objects = models.Manager()
    active_objects = ActiveManager()
    
    class Meta:
        verbose_name = u"Валюта"
        verbose_name_plural = u"Валюты"
    

