# -*- coding:utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.generic import GenericRelation

class Currency(models.Model):
    title = models.CharField(max_length = 50, verbose_name=u"Название")
    char_id = models.CharField(max_length = 3, verbose_name=u"Буквенное обозначение")
    symbol = models.CharField(max_length = 1, verbose_name=u"Символ")
    
    def __unicode__(self):
        return self.char_id

class Building(models.Model):
    LOCATION_CHOICES = (
        ('moscow', u'Москва'),
        ('country', u'Провинция'),
    )
    
    owner = models.ForeignKey(User, verbose_name=u"Владелец")
    town = models.CharField(max_length = 100, db_index=True, verbose_name=u"Город")
    location = models.CharField(max_length = 50, choices=LOCATION_CHOICES, null=False, blank=False, db_index=True, verbose_name=u"Местоположение", help_text=u"используется для url и для выбора html-формы")
    street = models.CharField(max_length = 100, verbose_name=u"Улица")
    house_id = models.CharField(max_length = 10, verbose_name=u"Номер дома")
    building_id = models.CharField(max_length = 10, null=True, blank=True, verbose_name=u"Строение")
    
    lat = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True, editable=False)
    lng = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True, editable=False)
    
    total_area = models.DecimalField(max_digits=8, decimal_places=3, null=True, blank=True, verbose_name=u"Общая площадь", help_text=u"площадь в м\u00B2")
    
    price = models.DecimalField(max_digits=12, decimal_places=2, db_index=True, verbose_name=u"Цена")
    currency = models.ForeignKey(Currency, verbose_name=u"Валюта")
    
    metro_remoteness_by_legs = models.PositiveSmallIntegerField(null=True, blank=True, verbose_name=u"до метро пешком", help_text=u"время в минутах")
    metro_remoteness_by_bus = models.PositiveSmallIntegerField(null=True, blank=True, verbose_name=u"до метро транспортом", help_text=u"время в минутах")
    mkad_remoteness = models.PositiveSmallIntegerField(null=True, blank=True, verbose_name=u"от МКАД", help_text=u"расстояние в километрах")
    nearest_metro_stations = models.CharField(max_length = 150, null=True, blank=True, verbose_name=u"ближайшие станции метро", help_text=u"перечислите через запятую")
    
    description = models.TextField(null=True, blank=True, verbose_name=u"Дополнительно")
    
    images = GenericRelation('images.ImagedItem')
    
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)
    deleted_at = models.DateTimeField(null=True, blank=True, editable=False)
    
    class Meta:
        abstract = True
    

# =========
# = Flats =
# =========
class HouseType(models.Model):
    title = models.CharField(max_length = 50, verbose_name=u"Тип дома")
    
    def __unicode__(self):
        return self.title

class RenovationType(models.Model):
    title = models.CharField(max_length = 50, verbose_name=u"Тип ремонта")
    
    def __unicode__(self):
        return self.title

class Flat(Building):
    ROOMS_COUNT_CHOICES = zip(xrange(1,11), map(str, xrange(1,11)))
    BALCONY_COUNT_CHOICES = zip(xrange(6), map(str, xrange(6)))
    BATHROOM_COUNT_CHOICES = zip(xrange(4), map(str, xrange(4)))
    
    house_type = models.ForeignKey(HouseType, verbose_name=u"Тип дома")
    renovation_type = models.ForeignKey(RenovationType, verbose_name=u"Тип ремонта")
    is_new = models.BooleanField(default=False, verbose_name=u"Новостройка")
    
    furniture = models.BooleanField(default=False, verbose_name=u"Мебель")
    fridge = models.BooleanField(default=False, verbose_name=u"Холодильник")
    wash_machine = models.BooleanField(default=False, verbose_name=u"Стиральная машина")
    separated_bathroom = models.BooleanField(default=False, verbose_name=u"Раздельный санузел")
    parking = models.BooleanField(default=False, verbose_name=u"Парковка")
    
    floor = models.PositiveSmallIntegerField(verbose_name=u"Этаж")
    floors_count = models.PositiveSmallIntegerField(verbose_name=u"Всего этажей")
    rooms_count = models.PositiveSmallIntegerField(db_index=True, choices=ROOMS_COUNT_CHOICES, verbose_name=u"Кол-во комнат")
    
    balcony_count = models.PositiveSmallIntegerField(default=0, choices=BALCONY_COUNT_CHOICES, verbose_name=u"Кол-во балконов")
    bathrooms_count = models.PositiveSmallIntegerField(default=1, choices=BATHROOM_COUNT_CHOICES, verbose_name=u"Кол-во ванных")
    
    kitchen_area = models.DecimalField(max_digits=8, decimal_places=3, null=True, blank=True, verbose_name=u"Площадь кухни", help_text=u"площадь в м\u00B2")
    
    class Meta:
        abstract = True
    

class RentFlat(Flat):
    PAYMENT_PERIOD_CHOICES = (
        ('month', u'месяц'),
        ('day', u'день'),
    )
    payment_period = models.CharField(max_length=10, choices=PAYMENT_PERIOD_CHOICES, verbose_name=u"Период оплаты")
    agent_commission = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, verbose_name=u"Комиссия агента", help_text=u"размер в %")
    
    pets = models.BooleanField(default=False, verbose_name=u"Можно с животными")
    children = models.BooleanField(default=False, verbose_name=u"Можно с детьми")
    
    def get_absolute_url(self):
        return "/buildings/rent/flats/%i/" % self.pk
    

class SellFlat(Flat):
    mortgage = models.BooleanField(default=False, verbose_name=u"Ипотека")
    
    part_in_flat = models.BooleanField(default=False, verbose_name=u"Доля в квартире")
    
    def get_absolute_url(self):
        return "/buildings/sell/flats/%i/" % self.pk
    

