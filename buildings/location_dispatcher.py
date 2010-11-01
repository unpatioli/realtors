# -*- coding:utf-8 -*-
from buildings import model_forms


LOCATION_FORMS = {
    'moscow': {
        'rent': {
            'form': model_forms.MoscowRentFlatForm,
            'detail_template': 'buildings/moscow_rentflat_detail.html',
        },
        # 'sell': {
        #     'form': model_forms.MoscowSellFlatForm,
        #     'detail_template': 'buildings/moscow_sellflat_detail.html',
        # },
        
        'instance_params': {
            'location': 'moscow',
            'town': u'Москва',
        },
    },
    
    'country': {
        'rent': {
            'form': model_forms.CountryRentFlatForm,
            'detail_template': 'buildings/country_rentflat_detail.html',
        },
        # 'sell': {
        #     'form': model_forms.CountrySellFlatForm,
        #     'detail_template': 'buildings/country_sellflat_detail.html',
        # },
        
        'instance_params': {
            'location': 'country',
        }
    },
}

# TODO Inherit LocationDispatcher from dict
class LocationDispatcher(object):
    def __init__(self, deal_type, location):
        self.deal_type, self.location = deal_type, location
    
    def location_valid(self):
        return self.location in LOCATION_FORMS
    
    @property
    def form_class(self):
        return LOCATION_FORMS[self.location][self.deal_type]['form']
    
    @property
    def instance_params(self):
        return LOCATION_FORMS[self.location]['instance_params']
    
    @property
    def detail_template(self):
        return LOCATION_FORMS[self.location][self.deal_type]['detail_template']
    

