# -*- coding:utf-8 -*-
from django import forms

from form_utils.widgets import DivCheckboxSelectMultiple
from buildings.models import Metro, ExtraParameters, RentFlat, SellFlat

class Baseform(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(Baseform, self).__init__(*args, **kwargs)
        # if 'nearest_metro_stations' in self.fields:
        #     self.fields['nearest_metro_stations'] = forms.ModelMultipleChoiceField(
        #                             queryset = Metro.objects.all(),
        #                             label = u"Ближайшие станции метро",
        #                             widget = DivCheckboxSelectMultiple(classes=['metro', 'scroll', 'reset']),
        #                             required = False
        #                     )
        if 'nearest_metro_stations' in self.fields:
            self.fields['nearest_metro_stations'].help_text = ""
        if 'extra_parameters' in self.fields:
            self.fields['extra_parameters'].help_text = ""
    class Meta:
        widgets = {
            'nearest_metro_stations': DivCheckboxSelectMultiple(classes=['metro', 'scroll']),
            'extra_parameters': DivCheckboxSelectMultiple(classes=['scroll']),
        }

# ==================
# = RentFlat forms =
# ==================
class RentFlatForm(Baseform):
    class Meta(Baseform.Meta):
        model = RentFlat
        fields = (
            'town', 'street', 'house_id', 'building_id',
            'metro_remoteness_by_legs', 'metro_remoteness_by_bus', 'mkad_remoteness', 'nearest_metro_stations',
            
            'house_type', 'renovation_type', 'is_new',
            
            'rooms_count', 'balcony_count',
            
            'total_area', 'kitchen_area',
            
            'floor', 'floors_count',
            
            'bathrooms_count',
            # 'furniture', 'fridge', 'wash_machine', 'separated_bathroom', 'parking', 'pets', 'children',
            'extra_parameters',
            
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
class SellFlatForm(Baseform):
    class Meta(Baseform.Meta):
        model = SellFlat
        fields = (
            'town', 'street', 'house_id', 'building_id',
            'metro_remoteness_by_legs', 'metro_remoteness_by_bus', 'mkad_remoteness', 'nearest_metro_stations',
            
            'house_type', 'renovation_type', 'is_new',
            
            'rooms_count', 'balcony_count',
            
            'total_area', 'kitchen_area',
            
            'floor', 'floors_count',
            
            'bathrooms_count',
            # 'furniture', 'fridge', 'wash_machine', 'separated_bathroom', 'parking',
            'extra_parameters',
            
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

