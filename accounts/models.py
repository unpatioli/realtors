# -*- coding:utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

class UserProfile(models.Model):
    GENDER_CHOICES = (
        (None, u'Выберите пол'),
        (True, u'Муж'),
        (False, u'Жен'),
    )
    
    user = models.ForeignKey(User, unique=True)
    
    birthday = models.DateField(null=True, blank=True, verbose_name=u"День рождения")
    gender = models.NullBooleanField(choices=GENDER_CHOICES, verbose_name=u"Пол")
    
    is_closed = models.BooleanField(default=False, db_index=True, verbose_name=u"Закрыть профиль")
    
    avatar = models.ImageField(upload_to='avatars', null=True, blank=True, verbose_name=u"Аватар")
    description = models.TextField(null=True, blank=True, verbose_name=u"Дополнительно")
    
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)
    deleted_at = models.DateTimeField(null=True, blank=True, editable=False)

class Realtor(models.Model):
    user = models.ForeignKey(User, unique=True)
    
    experience = models.PositiveSmallIntegerField(null=True, blank=True, verbose_name=u"Опыт работы")
    is_private = models.BooleanField(default=False, verbose_name=u"Частный риэлтор")
    agency_title = models.CharField(max_length = 150, null=True, blank=True, verbose_name=u"Агентство")
    
    in_sales = models.BooleanField(default=False, verbose_name=u"Продажа")
    in_rents = models.BooleanField(default=False, verbose_name=u"Аренда")
    in_camps = models.BooleanField(default=False, verbose_name=u"Загородная недвижимость")
    in_commercials = models.BooleanField(default=False, verbose_name=u"Коммерческая недвижимость")
    
    in_msk = models.BooleanField(default=True, db_index=True, verbose_name=u"Москва")
    in_country = models.BooleanField(default=False, db_index=True, verbose_name=u"Область")
    
    commission_from = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, verbose_name=u"Комиссия от")
    commission_to = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, verbose_name=u"Комиссия до")
    
    deal_commission = models.BooleanField(default=False, verbose_name=u"Договорная комиссия")
    
    phone = models.CharField(max_length = 50, null=True, blank=True, verbose_name=u"Телефон")
    
    rating = models.PositiveSmallIntegerField(default=0, verbose_name=u"Рейтинг")
    views_count = models.PositiveIntegerField(default=0, verbose_name=u"Кол-во просмотров")
    
    description = models.TextField(null=True, blank=True, verbose_name=u"Дополнительно")

# ===========
# = Signals =
# ===========
def user_created_handler(sender, instance, created, **kwargs):
    if created:
        instance.userprofile_set.create()

post_save.connect(user_created_handler, sender=User, dispatch_uid="users-profilecreation-signal")
