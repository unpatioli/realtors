# -*- coding:utf-8 -*-
from buildings import model_forms


LOCATION_FORMS = {
    'moscow': {
        'rent': {
            'form': model_forms.MoscowRentFlatForm,
            'detail_template': 'buildings/detail/moscow_rentflat_detail.html',
        },
        'sell': {
            'form': model_forms.MoscowSellFlatForm,
            'detail_template': 'buildings/detail/moscow_sellflat_detail.html',
        },
        
        'instance_params': {
            'location': 'moscow',
            'town': u'Москва',
        },
        
        'ru': 'Москва',
    },
    
    'moscow_region': {
        'rent': {
            'form': model_forms.MoscowRegionRentFlatForm,
            'detail_template': 'buildings/detail/moscow_region_rentflat_detail.html',
        },
        'sell': {
            'form': model_forms.MoscowRegionSellFlatForm,
            'detail_template': 'buildings/detail/moscow_region_sellflat_detail.html',
        },
        
        'instance_params': {
            'location': 'moscow_region',
        },
        
        'ru': 'Московская область',
    },
    
    'common': {
        'rent': {
            'form': model_forms.CommonRentFlatForm,
            'detail_template': 'buildings/detail/common_rentflat_detail.html',
        },
        'sell': {
            'form': model_forms.CommonSellFlatForm,
            'detail_template': 'buildings/detail/common_sellflat_detail.html',
        },
        
        'instance_params': {
            'location': 'common',
        },
        
        'ru': 'Страна',
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
    
    def localized_titles(self, lang='ru'):
        ordnung = ('moscow', 'moscow_region', 'common')
        return [(location, LOCATION_FORMS[location][lang]) for location in ordnung]
        # return [(location, LOCATION_FORMS[location][lang]) for location in LOCATION_FORMS]
    

