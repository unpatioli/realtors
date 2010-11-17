# -*- coding:utf-8 -*-
from django import forms

from buildings import widgets
from buildings.models import Metro, RentFlat, SellFlat

# ==================
# = RentFlat forms =
# ==================
class RentFlatForm(forms.ModelForm):
    nearest_metro_stations = forms.ModelMultipleChoiceField(
                                    queryset = Metro.objects.all(),
                                    label = u"Ближайшие станции метро",
                                    widget = widgets.DivCheckboxSelectMultiple(classes=['metro', 'scroll', 'reset']),
                                    required = False
                            )
    
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
    

class CommonRentFlatForm(RentFlatForm):
    class Meta(RentFlatForm.Meta):
        exclude = ('mkad_remoteness', 'metro_remoteness_by_legs', 'metro_remoteness_by_bus', 'nearest_metro_stations', )
    


# ==================
# = SellFlat forms =
# ==================
class SellFlatForm(forms.ModelForm):
    nearest_metro_stations = forms.ModelMultipleChoiceField(
                                    queryset = Metro.objects.all(),
                                    label = u"Ближайшие станции метро",
                                    widget = widgets.DivCheckboxSelectMultiple(classes=['metro', 'scroll', 'reset']),
                                    required = False
                            )
    
    class Meta:
        model = SellFlat
        fields = (
            'town', 'street', 'house_id', 'building_id',
            'metro_remoteness_by_legs', 'metro_remoteness_by_bus', 'mkad_remoteness', 'nearest_metro_stations',
            
            'house_type', 'renovation_type', 'is_new',
            
            'rooms_count', 'balcony_count',
            
            'total_area', 'kitchen_area',
            
            'floor', 'floors_count',
            
            'bathrooms_count',
            'furniture', 'fridge', 'wash_machine', 'separated_bathroom', 'parking',
            
            'price', 'currency',
            
            'mortgage', 'part_in_flat',
            
            'description',
        )
    

class MoscowSellFlatForm(SellFlatForm):
    class Meta(SellFlatForm.Meta):
        exclude = ('town', 'mkad_remoteness',)
    

class MoscowRegionSellFlatForm(SellFlatForm):
    class Meta(SellFlatForm.Meta):
        exclude = ('metro_remoteness_by_legs', 'metro_remoteness_by_bus', 'nearest_metro_stations', )
    

class CommonSellFlatForm(SellFlatForm):
    class Meta(SellFlatForm.Meta):
        exclude = ('mkad_remoteness', 'metro_remoteness_by_legs', 'metro_remoteness_by_bus', 'nearest_metro_stations', )
    

# ================
# = Form factory =
# ================
FORMS = {
    'moscow': {
        'rentflat': MoscowRentFlatForm,
        'sellflat': MoscowSellFlatForm,
    },
    'moscow_region': {
        'rentflat': MoscowRegionRentFlatForm,
        'sellflat': MoscowRegionSellFlatForm,
    },
    'common': {
        'rentflat': CommonRentFlatForm,
        'sellflat': CommonSellFlatForm,
    },
}
def form_factory(location, object_type):
    return FORMS[location][object_type]

