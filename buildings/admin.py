from django.contrib import admin
from buildings import models

admin.site.register(models.ExtraParameters)
admin.site.register(models.RentFlat)
admin.site.register(models.SellFlat)