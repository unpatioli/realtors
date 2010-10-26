# -*- coding:utf-8 -*-
from django.db import models
from django.contrib.auth.models import User

class Currency(models.Model):
    title = models.CharField(max_length = 50, verbose_name="Название")
    char_id = models.CharField(max_length = 3, verbose_name="Буквенное обозначение")
    symbol = models.CharField(max_length = 1, verbose_name="Символ")
    
    def __str__(self):
        return self.char_id

class Building(models.Model):
    owner = models.ForeignKey(User, verbose_name="Владелец")
    town = models.CharField(max_length = 100, db_index=True, verbose_name="Город")
    street = models.CharField(max_length = 100, verbose_name="Улица")
    house_id = models.CharField(max_length = 10, verbose_name="Номер дома")
    building_id = models.CharField(max_length = 10, null=True, blank=True, verbose_name="Строение")
    
    total_area = models.DecimalField(max_digits=8, decimal_places=3, null=True, blank=True, verbose_name="Общая площадь")
    
    price = models.DecimalField(max_digits=12, decimal_places=2, db_index=True, verbose_name="Цена")
    currency = models.ForeignKey(Currency, verbose_name="Валюта")
    
    metro_remoteness_by_legs = models.PositiveSmallIntegerField(null=True, blank=True, verbose_name="до метро пешком")
    metro_remoteness_by_bus = models.PositiveSmallIntegerField(null=True, blank=True, verbose_name="до метро транспортом")
    mkad_remoteness = models.PositiveSmallIntegerField(null=True, blank=True, verbose_name="от МКАД")
    nearest_metro_stations = models.CharField(max_length = 150, null=True, blank=True, verbose_name="ближайшие станции метро")
    
    description = models.TextField(null=True, blank=True, verbose_name="Дополнительно")
    
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)
    deleted_at = models.DateTimeField(null=True, blank=True, editable=False)
    
    class Meta:
        abstract = True
    

# =========
# = Flats =
# =========
class HouseType(models.Model):
    title = models.CharField(max_length = 50, verbose_name="Тип дома")
    
    def __str__(self):
        return self.title

class RenovationType(models.Model):
    title = models.CharField(max_length = 50, verbose_name="Тип ремонта")
    
    def __str__(self):
        return self.title

class Flat(Building):
    house_type = models.ForeignKey(HouseType, verbose_name="Тип дома")
    renovation_type = models.ForeignKey(RenovationType, verbose_name="Тип ремонта")
    is_new = models.BooleanField(default=False, verbose_name="Новостройка")
    
    furniture = models.BooleanField(default=False, verbose_name="Мебель")
    fridge = models.BooleanField(default=False, verbose_name="Холодильник")
    wash_machine = models.BooleanField(default=False, verbose_name="Стиральная машина")
    separated_bathroom = models.BooleanField(default=False, verbose_name="Раздельный санузел")
    parking = models.BooleanField(default=False, verbose_name="Парковка")
    
    floor = models.PositiveSmallIntegerField(verbose_name="Этаж")
    floors_count = models.PositiveSmallIntegerField(verbose_name="Всего этажей")
    rooms_count = models.PositiveSmallIntegerField(db_index=True, verbose_name="Кол-во комнат")
    
    balcony_count = models.PositiveSmallIntegerField(default=0, verbose_name="Кол-во балконов")
    bathrooms_count = models.PositiveSmallIntegerField(default=1, verbose_name="Кол-во ванных")
    
    kitchen_area = models.DecimalField(max_digits=8, decimal_places=3, null=True, blank=True, verbose_name="Площадь кухни")
    
    class Meta:
        abstract = True
    

class RentFlat(Flat):
    PAYMENT_PERIOD_CHOICES = (
        ('month', 'месяц'),
        ('day', 'день'),
    )
    payment_period = models.CharField(max_length=10, choices=PAYMENT_PERIOD_CHOICES, verbose_name="Период оплаты")
    agent_commission = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, verbose_name="Комиссия агента")
    
    pets = models.BooleanField(default=False, verbose_name="Можно с животными")
    children = models.BooleanField(default=False, verbose_name="Можно с детьми")

class SellFlat(Flat):
    mortgage = models.BooleanField(default=False, verbose_name="Ипотека")
    
    part_in_flat = models.BooleanField(default=False, verbose_name="Доля в квартире")

