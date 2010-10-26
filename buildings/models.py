from django.db import models
from django.contrib.auth.models import User

class Building(models.Model):
    owner = models.ForeignKey(User)
    town = models.CharField(max_length = 100, db_index=True)
    street = models.CharField(max_length = 100)
    house_id = models.CharField(max_length = 10)
    building_id = models.CharField(max_length = 10, null=True, blank=True)
    
    total_area = models.DecimalField(max_digits=8, decimal_places=3, null=True, blank=True)
    
    price = models.DecimalField(max_digits=12, decimal_places=2, db_index=True)
    
    metro_remoteness_by_legs = models.PositiveSmallIntegerField(null=True, blank=True)
    metro_remoteness_by_bus = models.PositiveSmallIntegerField(null=True, blank=True)
    mkad_remoteness = models.PositiveSmallIntegerField(null=True, blank=True)
    nearest_metro_stations = models.CharField(max_length = 150, null=True, blank=True)
    
    description = models.TextField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)
    deleted_at = models.DateTimeField(null=True, blank=True, editable=False)
    
    class Meta:
        abstract = True
    

# =========
# = Flats =
# =========
class HouseType(models.Model):
    title = models.CharField(max_length = 50)

class RenovationType(models.Model):
    title = models.CharField(max_length = 50)

class Flat(Building):
    house_type = models.ForeignKey(HouseType)
    renovation_type = models.ForeignKey(RenovationType)
    is_new = models.BooleanField(default=False)
    
    furniture = models.BooleanField(default=False)
    fridge = models.BooleanField(default=False)
    wash_machine = models.BooleanField(default=False)
    separated_bathroom = models.BooleanField(default=False)
    parking = models.BooleanField(default=False)
    
    floor = models.PositiveSmallIntegerField()
    floors_count = models.PositiveSmallIntegerField()
    rooms_count = models.PositiveSmallIntegerField(db_index=True)
    
    balcony_count = models.PositiveSmallIntegerField(default=0)
    bathrooms_count = models.PositiveSmallIntegerField(default=1)
    
    kitchen_area = models.DecimalField(max_digits=8, decimal_places=3, null=True, blank=True)
    
    class Meta:
        abstract = True
    

class RentFlat(Flat):
    is_daily_price = models.BooleanField(default=False)
    agent_commission = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    
    pets = models.BooleanField(default=False)
    children = models.BooleanField(default=False)

class SellFlat(Flat):
    mortgage = models.BooleanField(default=False)
    
    part_in_flat = models.BooleanField(default=False)

