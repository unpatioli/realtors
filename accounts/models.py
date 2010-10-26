from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    GENDER_CHOICES = (
        (None, 'Выберите пол'),
        (True, 'Муж'),
        (False, 'Жен'),
    )
    
    user = models.ForeignKey(User, unique=True)
    
    birthday = models.DateField(null=True, blank=True, verbose_name="День рождения")
    gender = models.NullBooleanField(choices=GENDER_CHOICES, verbose_name="Пол")
    
    is_closed = models.BooleanField(default=False, db_index=True, verbose_name="Закрыть профиль")
    
    avatar = models.ImageField(upload_to='avatars', null=True, blank=True, verbose_name="Аватар")
    description = models.TextField(null=True, blank=True, verbose_name="Дополнительно")
    
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)
    deleted_at = models.DateTimeField(null=True, blank=True, editable=False)

class Realtor(models.Model):
    user = models.ForeignKey(User, unique=True)
    
    experience = models.PositiveSmallIntegerField(null=True, blank=True, verbose_name="Опыт работы")
    is_private = models.BooleanField(default=False, verbose_name="Частный риэлтор")
    agency_title = models.CharField(max_length = 150, null=True, blank=True, verbose_name="Агентство")
    
    in_sales = models.BooleanField(default=False, verbose_name="Продажа")
    in_rents = models.BooleanField(default=False, verbose_name="Аренда")
    in_camps = models.BooleanField(default=False, verbose_name="Загородная недвижимость")
    in_commercials = models.BooleanField(default=False, verbose_name="Коммерческая недвижимость")
    
    in_msk = models.BooleanField(default=True, db_index=True, verbose_name="Москва")
    in_country = models.BooleanField(default=False, db_index=True, verbose_name="Область")
    
    commission_from = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, verbose_name="Комиссия от")
    commission_to = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, verbose_name="Комиссия до")
    
    deal_commission = models.BooleanField(default=False, verbose_name="Договорная комиссия")
    
    phone = models.CharField(max_length = 50, null=True, blank=True, verbose_name="Телефон")
    
    rating = models.PositiveSmallIntegerField(default=0, verbose_name="Рейтинг")
    views_count = models.PositiveIntegerField(default=0, verbose_name="Кол-во просмотров")
    
    description = models.TextField(null=True, blank=True, verbose_name="Дополнительно")

