from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    GENDER_CHOICES = (
        ('М', 'Муж'),
        ('Ж', 'Жен'),
    )
    
    user = models.ForeignKey(User, unique=True)
    
    birthday = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    
    is_closed = models.BooleanField(default=False)
    
    description = models.TextField(null=True, blank=True)
    
    avatar = models.ImageField(upload_to='users/avatars', null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)
    deleted_at = models.DateTimeField(null=True, blank=True, editable=False)

