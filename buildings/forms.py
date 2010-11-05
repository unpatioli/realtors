# -*- coding:utf-8 -*-
from django import forms
from buildings.models import Currency, HouseType, RenovationType, Flat, RentFlat

class SearchForm(forms.Form):
    # Price
    price_gt = forms.DecimalField(required=False)
    price_lt = forms.DecimalField(required=False)
    currency = forms.ModelChoiceField(queryset=Currency.objects.all(), required=False)
    
    # Publication
    with_photo = forms.BooleanField(required=False)
    period = forms.ChoiceField(choices=[(0,u'месяц'), (1,u'3 недели'), (2,u'2 недели'), (3,u'неделя'), (4,u'3 суток'), (5,u'сутки')], required=False)

class FlatSearchForm(SearchForm):
    # Object type and metrages
    rooms_count = forms.MultipleChoiceField(choices=Flat.ROOMS_COUNT_CHOICES, required=False)
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

class SellFlatSearchForm(FlatSearchForm):
    # Price
    mortgage = forms.BooleanField(required=False)
    part_in_flat = forms.BooleanField(required=False)

