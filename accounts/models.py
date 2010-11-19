# -*- coding:utf-8 -*-
from django.conf import settings
from django.db import models
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.db.models.signals import post_save

from image_utils.modelfields import ResizedImageField

class UserProfile(models.Model):
    GENDER_CHOICES = (
        (True, u'Мужской'),
        (False, u'Женский'),
    )
    
    user = models.ForeignKey(User, unique=True)
    
    birthday = models.DateField(null=True, blank=True, verbose_name=u"День рождения")
    gender = models.NullBooleanField(choices=GENDER_CHOICES, verbose_name=u"Пол")
    
    is_closed = models.BooleanField(default=False, db_index=True, verbose_name=u"Закрыть профиль")
    
    avatar = ResizedImageField(upload_to='avatars', dimensions=settings.AVATAR_SIZE, null=True, blank=True, verbose_name=u"Аватар")
    
    description = models.TextField(null=True, blank=True, verbose_name=u"Дополнительно")
    
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)
    deleted_at = models.DateTimeField(null=True, blank=True, editable=False)
    
    def __unicode__(self):
        if self.user.first_name == "" and self.user.last_name == "":
            return "%s's profile" % unicode(self.user)
        return self.get_name
    
    def get_name(self):
        return " ".join([self.user.first_name, self.user.last_name])
    
    def get_absolute_url(self):
        return reverse('accounts_profile', args=[self.user.pk])
    
    def can_show(self):
        return not self.is_closed
    

class Realtor(models.Model):
    EXPERIENCE_CHOICES = (
        (0, u'Нет опыта'),
        (1, u'1 год'),
        (3, u'3 года'),
        (4, u'более 4 лет'),
    )
    
    user = models.ForeignKey(User, unique=True)
    
    experience = models.PositiveSmallIntegerField(choices=EXPERIENCE_CHOICES, null=True, blank=True, verbose_name=u"Опыт работы")
    is_private = models.BooleanField(default=False, verbose_name=u"Частный риэлтор")
    agency_title = models.CharField(max_length = 150, null=True, blank=True, verbose_name=u"Агентство")
    
    in_sales = models.BooleanField(default=False, verbose_name=u"Продажа")
    in_rents = models.BooleanField(default=False, verbose_name=u"Аренда")
    in_camps = models.BooleanField(default=False, verbose_name=u"Загородная недвижимость")
    in_commercials = models.BooleanField(default=False, verbose_name=u"Коммерческая недвижимость")
    
    in_msk = models.BooleanField(default=True, db_index=True, verbose_name=u"Москва")
    in_msk_region = models.BooleanField(default=False, db_index=True, verbose_name=u"Область")
    
    commission_from = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, verbose_name=u"Комиссия от")
    commission_to = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, verbose_name=u"Комиссия до")
    
    deal_commission = models.BooleanField(default=False, verbose_name=u"Договорная комиссия")
    
    phone = models.CharField(max_length = 50, null=True, blank=True, verbose_name=u"Телефон")
    
    rating = models.PositiveSmallIntegerField(default=0, editable=False, verbose_name=u"Рейтинг")
    views_count = models.PositiveIntegerField(default=0, editable=False, verbose_name=u"Кол-во просмотров")
    
    description = models.TextField(null=True, blank=True, verbose_name=u"Дополнительно")
    
    def get_absolute_url(self):
        return reverse('accounts_profile_realtor', args=[self.user.pk])
    
    def can_show(self):
        return True
    


# Managers
class ModeratedAgenciesManager(models.Manager):
    def get_query_set(self):
        return super(ModeratedAgenciesManager, self).get_query_set().filter(is_moderated = True)
    

# Model
class Agency(models.Model):
    administrators = models.ManyToManyField(User, verbose_name=u"Администраторы")
    is_moderated = models.BooleanField(default=False, verbose_name=u"Проверено")
    
    town = models.CharField(max_length = 100, verbose_name=u"Город")
    title = models.CharField(max_length = 150, verbose_name=u"Название")
    address = models.CharField(max_length = 250, null=True, blank=True, verbose_name=u"Адрес")
    phone = models.CharField(max_length = 200, null=True, blank=True, verbose_name=u"Телефон")
    website = models.URLField(max_length = 200, verify_exists=True, null=True, blank=True, verbose_name=u"Сайт")
    email = models.EmailField(max_length = 75, null=True, blank=True, verbose_name=u"e-mail")
    label = ResizedImageField(upload_to='agency_labels', dimensions=settings.AGENCY_LABEL_SIZE, null=True, blank=True, verbose_name=u"Эмблема")
    staff_count = models.PositiveSmallIntegerField(null=True, blank=True, verbose_name=u"Кол-во сотрудников")
    establishment_year = models.PositiveSmallIntegerField(null=True, blank=True, verbose_name=u"На рынке с", help_text=u"года")
    description = models.TextField(null=True, blank=True, verbose_name=u"Дополнительно")
    
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)
    deleted_at = models.DateTimeField(null=True, blank=True, editable=False)
    
    def __unicode__(self):
        return self.title
    
    # ============
    # = Managers =
    # ============
    objects = models.Manager() # default manager
    moderated_objects = ModeratedAgenciesManager()
    
    def is_administrator(self, user):
        return user in self.administrators.all()
    
    def can_edit(self, user):
        return self.is_administrator(user)
    
    def get_absolute_url(self):
        return reverse('accounts_agency_detail', args=[self.pk])
    


# ===========
# = Signals =
# ===========
def user_created_handler(sender, instance, created, **kwargs):
    if created:
        instance.userprofile_set.create()

post_save.connect(user_created_handler, sender=User, dispatch_uid="users-profilecreation-signal")
