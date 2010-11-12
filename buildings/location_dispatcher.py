# -*- coding:utf-8 -*-
from buildings import model_forms
from buildings import forms


LOCATION_FORMS = {
    'moscow': {
        'rent': {
            'form': model_forms.MoscowRentFlatForm,
            'search_form': forms.MoscowRentFlatSearchForm,
            'search_form_template': 'buildings/search/moscow_rentflat_search_form.html',
            'detail_template': 'buildings/detail/moscow_rentflat_detail.html',
        },
        'sell': {
            'form': model_forms.MoscowSellFlatForm,
            'search_form': forms.MoscowSellFlatSearchForm,
            'search_form_template': 'buildings/search/moscow_sellflat_search_form.html',
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
            'search_form': forms.MoscowRegionRentFlatSearchForm,
            'search_form_template': 'buildings/search/moscow_region_rentflat_search_form.html',
            'detail_template': 'buildings/detail/moscow_region_rentflat_detail.html',
        },
        'sell': {
            'form': model_forms.MoscowRegionSellFlatForm,
            'search_form': forms.MoscowRegionSellFlatSearchForm,
            'search_form_template': 'buildings/search/moscow_region_sellflat_search_form.html',
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
            'search_form': forms.CommonRentFlatSearchForm,
            'search_form_template': 'buildings/search/common_rentflat_search_form.html',
            'detail_template': 'buildings/detail/common_rentflat_detail.html',
        },
        'sell': {
            'form': model_forms.CommonSellFlatForm,
            'search_form': forms.CommonSellFlatSearchForm,
            'search_form_template': 'buildings/search/common_sellflat_search_form.html',
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
    def search_form_class(self):
        return LOCATION_FORMS[self.location][self.deal_type]['search_form']
    
    @property
    def search_form_template(self):
        return LOCATION_FORMS[self.location][self.deal_type]['search_form_template']
    
    @property
    def detail_template(self):
        return LOCATION_FORMS[self.location][self.deal_type]['detail_template']
    
    @staticmethod
    def localized_titles(self, lang='ru'):
        ordnung = ('moscow', 'moscow_region', 'common')
        return [(location, LOCATION_FORMS[location][lang]) for location in ordnung]
        # return [(location, LOCATION_FORMS[location][lang]) for location in LOCATION_FORMS]
    
    @staticmethod
    def deal_types(lang='ru'):
        return [('rent', 'Аренда'), ('sell', 'Продажа')]
    

