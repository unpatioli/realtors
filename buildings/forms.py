# -*- coding:utf-8 -*-
from django import forms
from form_utils import widgets
from buildings.models import Currency, HouseType, RenovationType, Metro, Flat, RentFlat

class SearchForm(forms.Form):
    PERIOD_CHOICES = (
        (4*7,u'месяц'),
        (3*7,u'3 недели'),
        (2*7,u'2 недели'),
        (7,u'неделя'),
        (3,u'3 суток'),
        (1,u'сутки'),
    )
    # Price
    price_gt = forms.DecimalField(required=False)
    price_lt = forms.DecimalField(required=False)
    currency = forms.ModelChoiceField(queryset=Currency.objects.all(), required=False, empty_label=None)
    
    # Publication
    with_photo = forms.BooleanField(required=False)
    period = forms.ChoiceField(choices=PERIOD_CHOICES, required=False)

class FlatSearchForm(SearchForm):
    # Object type and metrages
    from copy import deepcopy
    ROOMS_COUNT_CHOICES = deepcopy(Flat.ROOMS_COUNT_CHOICES)
    ROOMS_COUNT_CHOICES[-1] = ( ROOMS_COUNT_CHOICES[-1][0],
                                ROOMS_COUNT_CHOICES[-1][1] + " и более" )
    
    rooms_count = forms.MultipleChoiceField(required=False,
                                            choices=ROOMS_COUNT_CHOICES,
                                            widget=widgets.DivCheckboxSelectMultiple(classes = ['rooms'])
                                        )
    total_area_gt = forms.DecimalField(required=False)
    total_area_lt = forms.DecimalField(required=False)
    
    kitchen_area_gt = forms.DecimalField(required=False)
    kitchen_area_lt = forms.DecimalField(required=False)
    
    # House
    floor_gt = forms.IntegerField(required=False)
    floor_lt = forms.IntegerField(required=False)
    floor_no_first = forms.BooleanField(required=False)
    floor_no_last = forms.BooleanField(required=False)
    house_type = forms.ModelChoiceField(queryset=HouseType.objects.all(), empty_label=u"Не важно", required=False)
    renovation_type = forms.ModelChoiceField(queryset=RenovationType.objects.all(), empty_label=u"Не важно", required=False)
    
    # Other params
    furniture = forms.BooleanField(required=False)
    balcony = forms.BooleanField(required=False)
    fridge = forms.BooleanField(required=False)
    wash_machine = forms.BooleanField(required=False)

# ===============
# = Form mixins =
# ===============
class MoscowFlatSearchForm(forms.Form):
    # Location
    # metro_remoteness_by_legs_gt = forms.IntegerField(required=False)
    # metro_remoteness_by_legs_lt = forms.IntegerField(required=False)
    metro_remoteness_by_legs = forms.IntegerField(required=False,
                                                widget=widgets.SliderWidget(attrs={
                                                    'class': 'slider',
                                                    'readonly': 1,
                                                })
                                            )
    
    # metro_remoteness_by_bus_gt = forms.IntegerField(required=False)
    # metro_remoteness_by_bus_lt = forms.IntegerField(required=False)
    metro_remoteness_by_bus = forms.IntegerField(required=False,
                                                widget=widgets.SliderWidget(attrs={
                                                    'class': 'slider',
                                                    'readonly': 1,
                                                })
                                            )
    
    nearest_metro_stations = forms.ModelMultipleChoiceField(
                                    queryset = Metro.objects.all(),
                                    label = u"Ближайшие станции метро",
                                    widget = widgets.DivCheckboxSelectMultiple(classes = ['metro', 'scroll']),
                                    required = False
                            )

class MoscowRegionFlatSearchForm(forms.Form):
    # Location
    town = forms.CharField(required=False)
    
    # mkad_remoteness_gt = forms.IntegerField(required=False)
    # mkad_remoteness_lt = forms.IntegerField(required=False)
    mkad_remoteness = forms.IntegerField(required=False,
                                        widget=widgets.SliderWidget(attrs={
                                            'class': 'slider',
                                            'readonly': 1,
                                        })
                                    )

class CommonFlatSearchForm(forms.Form):
    # Location
    town = forms.CharField(required=False)

# =============
# = RentFlats =
# =============
class RentFlatSearchForm(FlatSearchForm):
    # Price
    payment_period = forms.ChoiceField(choices=RentFlat.PAYMENT_PERIOD_CHOICES, required=False)
    
    # Other params
    pets = forms.BooleanField(required=False)
    children = forms.BooleanField(required=False)
    
    # Realtors
    agency = forms.BooleanField(required=False)
    private = forms.BooleanField(required=False)
    zero_commission = forms.BooleanField(required=False)

class MoscowRentFlatSearchForm(RentFlatSearchForm, MoscowFlatSearchForm):
    pass

class MoscowRegionRentFlatSearchForm(RentFlatSearchForm, MoscowRegionFlatSearchForm):
    pass

class CommonRentFlatSearchForm(RentFlatSearchForm, CommonFlatSearchForm):
    pass

# =============
# = SellFlats =
# =============
class SellFlatSearchForm(FlatSearchForm):
    # Price
    mortgage = forms.BooleanField(required=False)
    part_in_flat = forms.BooleanField(required=False)

class MoscowSellFlatSearchForm(SellFlatSearchForm, MoscowFlatSearchForm):
    pass

class MoscowRegionSellFlatSearchForm(SellFlatSearchForm, MoscowRegionFlatSearchForm):
    pass

class CommonSellFlatSearchForm(SellFlatSearchForm, CommonFlatSearchForm):
    pass


# ================
# = Form factory =
# ================
FORMS = {
    'moscow': {
        'rentflat': MoscowRentFlatSearchForm,
        'sellflat': MoscowSellFlatSearchForm,
    },
    'moscow_region': {
        'rentflat': MoscowRegionRentFlatSearchForm,
        'sellflat': MoscowRegionSellFlatSearchForm,
    },
    'common': {
        'rentflat': CommonRentFlatSearchForm,
        'sellflat': CommonSellFlatSearchForm,
    },
}
def form_factory(location, object_type):
    return FORMS[location][object_type]

