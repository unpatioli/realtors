from buildings.models import RentFlat, SellFlat

from django.forms import ModelForm

class RentFlatForm(ModelForm):
    class Meta:
        model = RentFlat
    

class SellFlatForm(ModelForm):
    class Meta:
        model = SellFlat
    

        