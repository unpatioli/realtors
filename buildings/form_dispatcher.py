# -*- coding:utf-8 -*-
from buildings import model_forms


LOCATION_FORMS = {
    'moscow': {
        'form': {
            'rent': model_forms.MoscowRentFlatForm,
            # 'sell': model_forms.MoscowSellFlatForm,
        },
        'instance_params': {
            'location': 'moscow',
            'town': u'Москва',
        },
    },
    
    'country': {
        'form': {
            'rent': model_forms.CountryRentFlatForm,
            # 'sell': model_forms.CountrySellFlatForm,
        },
        'instance_params': {
            'location': 'country',
        }
    },
}

class FormDispatcher(object):
    def __init__(self, deal_type, location):
        self.deal_type, self.location = deal_type, location
    
    def location_valid(self):
        return self.location in LOCATION_FORMS
    
    @property
    def form_class(self):
        return LOCATION_FORMS[self.location]['form'][self.deal_type]
    
    @property
    def instance_params(self):
        return LOCATION_FORMS[self.location]['instance_params']

