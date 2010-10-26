from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    GENDER_CHOICES = (
        (None, 'Выберите пол'),
        (True, 'Муж'),
        (False, 'Жен'),
    )
    
    user = models.ForeignKey(User, unique=True)
    
    birthday = models.DateField(null=True, blank=True)
    gender = models.NullBooleanField(choices=GENDER_CHOICES)
    
    is_closed = models.BooleanField(default=False, db_index=True)
    
    avatar = models.ImageField(upload_to='avatars', null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)
    deleted_at = models.DateTimeField(null=True, blank=True, editable=False)

class Realtor(models.Model):
    user = models.ForeignKey(User, unique=True)
    
    experience = models.PositiveSmallIntegerField(null=True, blank=True)
    is_private = models.BooleanField(default=False)
    agency_title = models.CharField(max_length = 150, null=True, blank=True)
    
    in_sales = models.BooleanField(default=False)
    in_rents = models.BooleanField(default=False)
    in_camps = models.BooleanField(default=False)
    in_commercials = models.BooleanField(default=False)
    
    in_msk = models.BooleanField(default=True, db_index=True)
    in_country = models.BooleanField(default=False, db_index=True)
    
    commission_from = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    commission_to = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    
    deal_commission = models.BooleanField(default=False)
    
    phone = models.CharField(max_length = 50, null=True, blank=True)
    
    rating = models.PositiveSmallIntegerField(default=0)
    views_count = models.PositiveIntegerField(default=0)
    
    description = models.TextField(null=True, blank=True)

