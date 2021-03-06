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

def user_object_list(request, user_id, location='moscow', object_type='rentflat'):
    from django.contrib.auth.models import User
    
    user = get_object_or_404(User, pk=user_id)
    model = ContentType.objects.get(model=object_type).model_class()
    queryset = model.objects.filter(owner__pk=user_id, location=location)
    queryset = _apply_sort(queryset, request.GET, model)
    return object_list(
        request,
        queryset = queryset,
        template_name = 'buildings/%s_%s_list.html' % (location, object_type),
        extra_context = {
            'show_management_panel': request.user.id == int(user_id),
            'is_user_list': True,
            'user': user,
            'user_is_realtor': request.user.is_authenticated() and request.user.realtor_set.exists(),
            
            'locations': LocationDispatcher.localized_titles('ru'),
            'location': location,
            
            'object_types': LocationDispatcher.object_types(),
            'object_type': object_type,
        }
    )

def agency_object_list(request, agency_id, location='moscow', object_type='rentflat'):
    from accounts.models import Agency
    
    agency = get_object_or_404(Agency, pk=agency_id)
    model = ContentType.objects.get(model=object_type).model_class()
    queryset = model.objects.filter(owner__realtor__agencies__id = agency_id, location = location).select_related()
    queryset = _apply_sort(queryset, request.GET, model)
    
    return object_list(
        request,
        queryset = queryset,
        template_name = 'buildings/%s_%s_list.html' % (location, object_type),
        extra_context = {
            'is_agency_list': True,
            'agency': agency,
            
            'locations': LocationDispatcher.localized_titles('ru'),
            'location': location,
            
            'object_types': LocationDispatcher.object_types(),
            'object_type': object_type,
            
            'user_is_realtor': request.user.is_authenticated() and request.user.realtor_set.exists(),
        }
    )

def object_detail(request, location, object_type, id):
    from currencies.models import Currency
    
    model = ContentType.objects.get(model=object_type).model_class()
    obj = get_object_or_404(model, pk=id)
    
    obj_currency = obj.currency
    obj_price_eur = float(obj.price) / float(obj_currency.rate)
    currencies = Currency.active_objects.all()
    other_prices = [(currency.symbol, obj_price_eur * float(currency.rate)) for currency in currencies if currency != obj_currency]
    
    return direct_to_template(
        request,
        template = 'buildings/detail/%s_%s_detail.html' % (location, object_type),
        extra_context = {
            'object': obj,
            'show_object_controls': obj.can_edit(request.user),
            
            'location': location,
            'object_type': object_type,
            
            'other_prices': other_prices,
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

@login_required
def object_delete(request, location, object_type, id):
    model = ContentType.objects.get(model=object_type).model_class()
    obj = get_object_or_404(model, pk=id)
    if not obj.can_edit(request.user):
        raise Http404
    if request.method == "POST":
        obj.delete()
        messages.success(request, u"Объект успешно удален")
        return redirect(user_object_list, request.user.pk, location, object_type)
    return direct_to_template(
        request,
        template = "buildings/object_confirm_delete.html",
        extra_context = {
            'object': obj,
            'user_id': request.user.pk,
            'location': location,
            'object_type': object_type
        }
    )


# ==========
# = Search =
# ==========
def object_search(request, location='moscow', object_type='rentflat'):
    if request.method != 'GET':
        raise Http404
    
    params = request.GET.copy()
    if 'search' in params:
        is_submitted = True
        del params['search']
    else:
        is_submitted = False
    form_class = forms.form_factory(location, object_type)
    if is_submitted:
        form = form_class(request.GET)
        if form.is_valid():
            res = find.__dict__['%s_%s_find' % (location, object_type)](form)
            model = ContentType.objects.get(model=object_type).model_class()
            res = _apply_sort(res, params, model)
            return direct_to_template(
                request,
                template = 'buildings/%s_%s_list.html' % (location, object_type),
                extra_context = {
                    'object_list': res,
                    
                    'location': location,
                    'object_type': object_type,
                    
                    'is_search_result': True,
                    'q_string': params.urlencode(),
                    
                    'user_is_realtor': request.user.is_authenticated() and request.user.realtor_set.exists(),
                }
            )
    else:
        form = form_class(params)
    return direct_to_template(
        request,
        template = 'buildings/search/%s_%s_search_form.html' % (location, object_type),
        extra_context = {
            'form': form,
            
            'locations': LocationDispatcher.localized_titles('ru'),
            'location': location,
            
            'object_types': LocationDispatcher.object_types(),
            'object_type': object_type,
            
            'q_string': params.urlencode()
        }
    )

# =========
# = Utils =
# =========
def _apply_sort(queryset, params, model):
    if 'sort' in params and params['sort'] in model.FIELDS_ALLOWED_TO_SORT:
        queryset = queryset.order_by(model.FIELDS_ALLOWED_TO_SORT[params['sort']])
    return queryset

