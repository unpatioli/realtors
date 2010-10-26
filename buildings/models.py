from django.db import models

class Rieltor(models.Model):
    # user relation
    experience = models.PositiveIntegerField(null=True, blank=True)
    is_private = models.BooleanField(default=False)
    agency_title = models.CharField(max_length = 150, null=True, blank=True)
    
    in_sales = models.BooleanField(default=False)
    in_rents = models.BooleanField(default=False)
    in_camps = models.BooleanField(default=False)
    in_commercials = models.BooleanField(default=False)
    
    in_msk = models.BooleanField(default=True)
    in_country = models.BooleanField(default=False)
    
    commission_from = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    commission_to = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    
    deal_commission = models.BooleanField(default=False)
    
    phone = models.CharField(max_length = 50, null=True, blank=True)
    
    description = models.TextField(null=True, blank=True)
    
    rating = models.PositiveIntegerField(default=0)
    views_count = models.PositiveIntegerField(default=0)
    is_closed = models.BooleanField(default=0)
    
    avatar_file_name = models.CharField(null=True, blank=True)


class Building(models.Model):
    # rieltor relation
    town = models.CharField(max_length = 100)
    street = models.CharField(max_length = 100)
    house_id = models.CharField(max_length = 10)
    building_id = models.CharField(max_length = 10, null=True, blank=True)
    
    total_area = models.DecimalField(max_digits=8, decimal_places=3, null=True, blank=True)
    
    price = models.DecimalField(max_digits=12, decimal_places=2)
    
    metro_remoteness_by_legs = models.PositiveIntegerField(null=True, blank=True)
    metro_remoteness_by_bus = models.PositiveIntegerField(null=True, blank=True)
    mkad_remoteness = models.PositiveIntegerField(null=True, blank=True)
    nearest_metro_stations = models.CharField(max_length = 150, null=True, blank=True)
    
    description = models.TextField(null=True, blank=True)
    
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
    
    floor = models.PositiveIntegerField()
    floors_count = models.PositiveIntegerField()
    rooms_count = models.PositiveIntegerField()
    
    balcony_count = models.PositiveIntegerField(default=0)
    bathrooms_count = models.PositiveIntegerField(default=1)
    
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

