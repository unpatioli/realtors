# -*- coding:utf-8 -*-
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from django.views.generic.simple import direct_to_template
from django.views.generic.list_detail import object_list
from django.contrib import messages

from buildings.location_dispatcher import LocationDispatcher
from buildings import model_forms, forms, find

def user_object_list(request, user_id, location, object_type):
    model = ContentType.objects.get(model=object_type).model_class()
    
    return object_list(
        request,
        queryset = model.objects.filter(owner__pk=user_id, location=location),
        template_name = 'buildings/%s_%s_list.html' % (location, object_type),
        extra_context = {
            'show_management_panel': request.user.id == int(user_id),
            'user_id': user_id,
            
            'locations': LocationDispatcher.localized_titles('ru'),
            'location': location,
            
            'object_types': LocationDispatcher.object_types(),
            'object_type': object_type,
        }
    )

def object_detail(request, location, object_type, id):
    model = ContentType.objects.get(model=object_type).model_class()
    obj = get_object_or_404(model, pk=id)
    
    return direct_to_template(
        request,
        template = 'buildings/detail/%s_%s_detail.html' % (location, object_type),
        extra_context = {
            'object': obj,
            'show_object_controls': obj.can_edit(request.user),
            
            'location': location,
            'object_type': object_type,
        }
    )

@login_required
def object_new(request, location, object_type):
    model = ContentType.objects.get(model=object_type).model_class()
    form_class = model_forms.form_factory(location, object_type)
    if request.method == 'POST':
        instance_params = {'location': location}
        if location == 'moscow':
            instance_params['town'] = u'Москва'
        instance = model(owner=request.user, **instance_params)
        form = form_class(request.POST, instance=instance)
        if form.is_valid():
            obj = form.save()
            messages.success(request, u"Объект сохранен")
            return redirect(obj)
        else:
            messages.error(request, u"Объект не сохранен")
    else:
        form = form_class()
    return direct_to_template(
        request,
        template = "buildings/object_form.html",
        extra_context = {
            'form': form,
            
            'locations': LocationDispatcher.localized_titles('ru'),
            'location': location,
            
            'object_types': LocationDispatcher.object_types(),
            'object_type': object_type,
        }
    )

@login_required
def object_edit(request, location, object_type, id):
    model = ContentType.objects.get(model=object_type).model_class()
    obj = get_object_or_404(model, pk=id)
    if not obj.can_edit(request.user):
        raise Http404
    
    form_class = model_forms.form_factory(location, object_type)
    if request.method == 'POST':
        form = form_class(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            messages.success(request, u"Информация об объекте обновлена")
            return redirect(obj)
        else:
            messages.error(request, u"Информация об объекте не обновлена")
    else:
        form = form_class(instance=obj)
    return direct_to_template(
        request,
        template = "buildings/object_form.html",
        extra_context = {
            'form': form,
            
            'object_types': LocationDispatcher.object_types(),
            'object_type': object_type
        }
    )



# ==========
# = Search =
# ==========
def moscow_rentflat_search(request):
    return __flat_search(
                request,
                forms.MoscowRentFlatSearchForm,
                'buildings/search/moscow_rentflat_search_form.html',
                find.moscow_rentflat_find,
                'buildings/moscow_rentflat_list.html'
            )

def moscow_region_rentflat_search(request):
    return __flat_search(
                request,
                forms.MoscowRegionRentFlatSearchForm,
                'buildings/search/moscow_region_rentflat_search_form.html',
                find.moscow_region_rentflat_find,
                'buildings/moscow_region_rentflat_list.html'
            )

def common_rentflat_search(request):
    return __flat_search(
                request,
                forms.CommonRentFlatSearchForm,
                'buildings/search/common_rentflat_search_form.html',
                find.common_rentflat_find,
                'buildings/common_rentflat_list.html'
            )


def moscow_sellflat_search(request):
    return __flat_search(
                request,
                forms.MoscowSellFlatSearchForm,
                'buildings/search/moscow_sellflat_search_form.html',
                find.moscow_sellflat_find,
                'buildings/moscow_sellflat_list.html'
            )

def moscow_region_sellflat_search(request):
    return __flat_search(
                request,
                forms.MoscowRegionSellFlatSearchForm,
                'buildings/search/moscow_region_sellflat_search_form.html',
                find.moscow_region_sellflat_find,
                'buildings/moscow_region_sellflat_list.html'
            )

def common_sellflat_search(request):
    return __flat_search(
                request,
                forms.CommonSellFlatSearchForm,
                'buildings/search/common_sellflat_search_form.html',
                find.common_sellflat_find,
                'buildings/common_sellflat_list.html'
            )



def __flat_search(request, form_class, form_template, find_function, result_template):
    if request.method != 'GET':
        raise Http404
    
    if request.GET:
        form = form_class(request.GET)
        if form.is_valid():
            res = find_function(form)
            return direct_to_template(
                request,
                template = result_template,
                extra_context = {'res': res}
            )
    else:
        form = form_class()
    return direct_to_template(
        request,
        template = form_template,
        extra_context = {'form': form}
    )

