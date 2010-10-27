from buildings.models import RentFlat, SellFlat

from django.forms import ModelForm

# ==================
# = RentFlat forms =
# ==================
class RentFlatForm(ModelForm):
    class Meta:
        model = RentFlat
        fields = ('town', 'street', 'house_id', 'building_id', 'total_area', 'price', 'currency', 'metro_remoteness_by_legs', 'metro_remoteness_by_bus', 'mkad_remoteness', 'nearest_metro_stations', 'description', 'house_type', 'renovation_type', 'is_new', 'furniture', 'fridge', 'wash_machine', 'separated_bathroom', 'parking', 'floor', 'floors_count', 'rooms_count', 'balcony_count', 'bathrooms_count', 'kitchen_area', 'payment_period', 'agent_commission', 'pets', 'children',)
    
class MoscowRentFlatForm(RentFlatForm):
    class Meta(RentFlatForm.Meta):
        exclude = ('town', 'mkad_remoteness',)
    

class CountryRentFlatForm(RentFlatForm):
    class Meta(RentFlatForm.Meta):
        exclude = ('metro_remoteness_by_legs', 'metro_remoteness_by_bus', 'nearest_metro_stations', )


# ==================
# = SellFlat forms =
# ==================
class SellFlatForm(ModelForm):
    class Meta:
        model = SellFlat
    

        