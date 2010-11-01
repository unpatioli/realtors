from buildings.models import RentFlat, SellFlat

from django.forms import ModelForm

# ==================
# = RentFlat forms =
# ==================
class RentFlatForm(ModelForm):
    class Meta:
        model = RentFlat
        fields = (
            'town', 'street', 'house_id', 'building_id',
            'metro_remoteness_by_legs', 'metro_remoteness_by_bus', 'mkad_remoteness', 'nearest_metro_stations',
            
            'house_type', 'renovation_type', 'is_new',
            
            'rooms_count', 'balcony_count',
            
            'total_area', 'kitchen_area',
            
            'floor', 'floors_count',
            
            'bathrooms_count',
            'furniture', 'fridge', 'wash_machine', 'separated_bathroom', 'parking', 'pets', 'children',
            
            'price', 'currency', 'payment_period', 'agent_commission',
            
            'description',
            )
    
class MoscowRentFlatForm(RentFlatForm):
    class Meta(RentFlatForm.Meta):
        exclude = ('town', 'mkad_remoteness',)
    

class MoscowRegionRentFlatForm(RentFlatForm):
    class Meta(RentFlatForm.Meta):
        exclude = ('metro_remoteness_by_legs', 'metro_remoteness_by_bus', 'nearest_metro_stations', )


# ==================
# = SellFlat forms =
# ==================
class SellFlatForm(ModelForm):
    class Meta:
        model = SellFlat
    

        