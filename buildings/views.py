from buildings.models import RentFlat, SellFlat

from django.views.generic.simple import direct_to_template
from django.views.generic.list_detail import object_list
from django.views.generic.create_update import create_object, update_object

def rent_flats_list(request):
    return object_list(
        request,
        queryset=RentFlat.objects.all()
    )

