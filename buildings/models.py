# -*- coding:utf-8 -*-
from django.db import models
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.generic import GenericRelation

from currencies.models import Currency, get_rate

class Metro(models.Model):
    town = models.CharField(max_length = 100, db_index=True, verbose_name=u"Город")
    title = models.CharField(max_length = 100, db_index=True, verbose_name=u"Название станции")
    
    def __unicode__(self):
        return self.title
    

class ExtraParameters(models.Model):
    title = models.CharField(max_length=100, verbose_name=u"Название параметра")
    image = models.ImageField(upload_to='param_pictures', null=True, blank=True, verbose_name=u"Пиктограмма")
    
    content_types = models.ManyToManyField(ContentType, limit_choices_to = {'model__in': ['rentflat', 'sellflat']}, verbose_name=u"Модели")
    
    def __unicode__(self):
        return self.title
    
    class Meta:
        verbose_name = u"Дополнительный параметр"
        verbose_name_plural = u"Дополнительные параметры"
    

# ============
# = Building =
# ============

# Managers
class SearchableManager(models.Manager):
    def get_query_set(self):
        return super(SearchableManager, self).get_query_set().filter(price_EUR__isnull = False)
    

class LocationManager(SearchableManager):
    def __init__(self, location, *args, **kwargs):
        super(LocationManager, self).__init__(*args, **kwargs)
        self.location = location
    
    def get_query_set(self):
        return super(LocationManager, self).get_query_set().filter(location = self.location)
    

class NotSearchableManager(models.Manager):
    def get_query_set(self):
        return super(NotSearchableManager, self).get_query_set().filter(price_EUR__isnull = True)
    


# Model
class Building(models.Model):
    LOCATION_CHOICES = (
        ('moscow', u'Москва'),
        ('moscow_region', u'Область'),
        ('common', u'Другой регион'),
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
    
    price = models.DecimalField(max_digits=12, decimal_places=2, verbose_name=u"Цена")
    currency = models.ForeignKey(Currency, verbose_name=u"Валюта")
    
    price_EUR = models.PositiveIntegerField(null=True, blank=True, db_index=True, editable=False)
    
    metro_remoteness_by_legs = models.PositiveSmallIntegerField(null=True, blank=True, verbose_name=u"до метро пешком", help_text=u"время в минутах")
    metro_remoteness_by_bus = models.PositiveSmallIntegerField(null=True, blank=True, verbose_name=u"до метро транспортом", help_text=u"время в минутах")
    mkad_remoteness = models.PositiveSmallIntegerField(null=True, blank=True, verbose_name=u"от МКАД", help_text=u"расстояние в километрах")
    nearest_metro_stations = models.ManyToManyField(Metro, null=True, blank=True, verbose_name=u"Ближайшие станции метро")
    
    description = models.TextField(null=True, blank=True, verbose_name=u"Дополнительно")
    
    images = GenericRelation('images.ImagedItem')
    
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)
    deleted_at = models.DateTimeField(null=True, blank=True, editable=False)
    
    FIELDS_ALLOWED_TO_SORT = {
        'total_area': 'total_area',
        '-total_area': '-total_area',
    }
    
    def __unicode__(self):
        return u"Объект"
    
    def save(self, *args, **kwargs):
        char_id = self.currency.char_id
        try:
            rate = get_rate(char_id)
            self.price_EUR = int(self.price / rate)
            if 'payment_period' in self._meta.get_all_field_names():
                self.price_EUR /= self.payment_period
        except Exception as e:
            raise e
        super(Building, self).save(*args, **kwargs)
    
    
    # ============
    # = Managers =
    # ============
    objects = models.Manager()
    moscow_objects = LocationManager(location='moscow')
    moscow_region_objects = LocationManager(location='moscow_region')
    common_objects = LocationManager(location = 'common')
    
    not_searchable = NotSearchableManager()
    
    class Meta:
        abstract = True
    
    @property
    def get_address(self):
        address = filter(None, [self.street, self.house_id, self.building_id])
        return ", ".join(address)
    
    def can_edit(self, user):
        return self.owner == user
    

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
    __MAX_ROOMS_COUNT = 7
    ROOMS_COUNT_CHOICES = zip(
            xrange(1,__MAX_ROOMS_COUNT + 1), 
            map(str, xrange(1,__MAX_ROOMS_COUNT + 1))
        )
    
    BALCONY_COUNT_CHOICES = zip(xrange(6), map(str, xrange(6)))
    BATHROOM_COUNT_CHOICES = zip(xrange(4), map(str, xrange(4)))
    
    house_type = models.ForeignKey(HouseType, verbose_name=u"Тип дома")
    renovation_type = models.ForeignKey(RenovationType, verbose_name=u"Тип ремонта")
    is_new = models.BooleanField(default=False, verbose_name=u"Новостройка")
    
    # furniture = models.BooleanField(default=False, verbose_name=u"Мебель")
    # fridge = models.BooleanField(default=False, verbose_name=u"Холодильник")
    # wash_machine = models.BooleanField(default=False, verbose_name=u"Стиральная машина")
    # separated_bathroom = models.BooleanField(default=False, verbose_name=u"Раздельный санузел")
    # parking = models.BooleanField(default=False, verbose_name=u"Парковка")
    
    floor = models.PositiveSmallIntegerField(verbose_name=u"Этаж")
    floors_count = models.PositiveSmallIntegerField(verbose_name=u"Всего этажей")
    rooms_count = models.PositiveSmallIntegerField(db_index=True, choices=ROOMS_COUNT_CHOICES, verbose_name=u"Кол-во комнат")
    
    balcony_count = models.PositiveSmallIntegerField(default=0, choices=BALCONY_COUNT_CHOICES, verbose_name=u"Кол-во балконов")
    bathrooms_count = models.PositiveSmallIntegerField(default=1, choices=BATHROOM_COUNT_CHOICES, verbose_name=u"Кол-во ванных")
    
    kitchen_area = models.DecimalField(max_digits=8, decimal_places=3, null=True, blank=True, verbose_name=u"Площадь кухни", help_text=u"площадь в м\u00B2")
    
    Building.FIELDS_ALLOWED_TO_SORT.update({
        'rooms_count': 'rooms_count',
        '-rooms_count': '-rooms_count',
    })
    
    class Meta:
        abstract = True
    
    def clean(self):
        from django.core.exceptions import ValidationError
        if self.floors_count and self.floor > self.floors_count:
            raise ValidationError(u"Этаж не может быть больше количества этажей")
        if self.total_area and self.kitchen_area > self.total_area:
            raise ValidationError(u"Площадь кухни не может превышать общую площадь")
    

class RentFlat(Flat):
    PAYMENT_PERIOD_CHOICES = (
        (31, u'месяц'),
        (1, u'день'),
    )
    payment_period = models.PositiveSmallIntegerField(choices=PAYMENT_PERIOD_CHOICES, verbose_name=u"Период оплаты")
    
    agent_commission = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, verbose_name=u"Комиссия агента", help_text=u"размер в %")
    
    # pets = models.BooleanField(default=False, verbose_name=u"Можно с животными")
    # children = models.BooleanField(default=False, verbose_name=u"Можно с детьми")
    
    extra_parameters = models.ManyToManyField(ExtraParameters, limit_choices_to = {'content_types__model': 'rentflat'}, null=True, blank=True,  verbose_name=u"Дополнительные параметры")
    
    Flat.FIELDS_ALLOWED_TO_SORT.update({
        'commission': 'agent_commission',
        '-commission': '-agent_commission',
    })
    
    # def save(self, *args, **kwargs):
    #     self.price_EUR /= self.payment_period
    #     super(RentFlat, self).save(*args, **kwargs)
    
    class Meta(Flat.Meta):
        verbose_name = u"Квартира в аренду"
        verbose_name_plural = u"Квартиры в аренду"
    
    def get_absolute_url(self):
        return reverse('buildings_object_detail', args=[self.location, 'rentflat', self.pk])
    

class SellFlat(Flat):
    mortgage = models.BooleanField(default=False, verbose_name=u"Ипотека")
    
    extra_parameters = models.ManyToManyField(ExtraParameters, limit_choices_to = {'content_types__model': 'sellflat'}, null=True, blank=True, verbose_name=u"Дополнительные параметры")
    
    part_in_flat = models.BooleanField(default=False, verbose_name=u"Доля в квартире")
    
    class Meta(Flat.Meta):
        verbose_name = u"Квартира для продажи"
        verbose_name_plural = u"Квартиры для продажи"
    
    def get_absolute_url(self):
        return reverse('buildings_object_detail', args=[self.location, 'sellflat', self.pk])
    

