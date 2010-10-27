from buildings.models import RentFlat, SellFlat

from django.forms import ModelForm

class RentFlatForm(ModelForm):
    class Meta:
        model = RentFlat
        exclude = ('owner',)
    

class SellFlatForm(ModelForm):
    class Meta:
        model = SellFlat
    

        