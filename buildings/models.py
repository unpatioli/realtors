from django.db import models

class Rieltor(models.Model):
    # user relation
    experience = models.IntField()
    is_private = models.BooleanField()
    agency_title = models.CharField()
    
    in_sales = models.BooleanField()
    in_rents = models.BooleanField()
    in_camps = models.BooleanField()
    in_commercials = models.BooleanField()
    
    in_msk = models.BooleanField()
    in_country = models.BooleanField()
    
    commission_from = models.DecimalField()
    commission_to = models.DecimalField()
    
    deal_commission = models.BooleanField()
    
    phone = models.CharField()
    
    description = models.TextField()
    
    rating = models.IntField()
    views_count = models.IntField()
    is_closed = models.BooleanField()
    
    avatar_file_name = models.CharField()


class Building(models.Model):
    # rieltor relation
    town = models.CharField()
    street = models.CharField()
    house_id = models.CharField()
    building_id = models.CharField()
    
    total_area = models.DecimalField()
    
    price = models.DecimalField()
    
    metro_remoteness_by_legs = models.IntField()
    metro_remoteness_by_bus = models.IntField()
    mkad_remoteness = models.IntField()
    nearest_metro_stations = models.CharField()
    
    description = models.TextField()
    
    class Meta:
        abstract = True
    

# =========
# = Flats =
# =========
class Flat(Building):
    building_type = models.CharField()
    house_type = models.CharField()
    renovation_type = models.CharField()
    is_new = models.BooleanField()
    
    furniture = models.BooleanField()
    balcony = models.BooleanField()
    fridge = models.BooleanField()
    wash_machine = models.BooleanField()
    separated_bathroom = models.BooleanField()
    parking = models.BooleanField()
    
    floor = models.IntField()
    floors_count = models.IntField()
    
    rooms_count = models.IntField()
    balcony_count = models.IntField()
    bathrooms_count = models.IntField()
    
    kitchen_area = models.DecimalField()
    
    class Meta:
        abstract = True
    

class RentFlat(Flat):
    is_daily_price = models.BooleanField()
    agent_commission = models.DecimalField()
    
    pets = models.BooleanField()
    children = models.BooleanField()

class SellFlat(Flat):
    mortgage = models.BooleanField()
    
    part_in_flat = models.BooleanField()
