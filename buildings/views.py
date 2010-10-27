from buildings.models import RentFlat, SellFlat

from django.views.generic.simple import direct_to_template
from django.views.generic.list_detail import object_list, object_detail
from django.views.generic.create_update import create_object, update_object

def rentflat_list(request):
    return object_list(
        request,
        queryset = RentFlat.objects.all(),
        template_object_name = 'flat'
    )

def rentflat_detail(request, id):
    return object_detail(
        request,
        queryset = RentFlat.objects.all(),
        object_id = id,
        template_object_name = 'flat'
    )