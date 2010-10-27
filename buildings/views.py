from buildings.models import RentFlat, SellFlat

from django.views.generic.simple import direct_to_template
from django.views.generic.create_update import create_object, update_object

def rent_flats_list(request):
    rent_flats = RentFlat.objects.all()
    return direct_to_template(
        request,
        template='buildings/rent_flats_list.html',
        extra_context={'rent_flats': rent_flats}
    )

