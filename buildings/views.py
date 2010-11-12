# -*- coding:utf-8 -*-
from buildings.models import RentFlat, SellFlat
from buildings.location_dispatcher import LocationDispatcher
from buildings.forms import RentFlatSearchForm

from django.http import Http404
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views.generic.simple import direct_to_template, redirect_to
from django.views.generic.list_detail import object_list


# ============
# = RentFlat =
# ============
def user_rentflat_list(request, user_id):
    return object_list(
        request,
        queryset = RentFlat.objects.filter(owner__pk__exact=user_id),
        extra_context = {
            'objects_type': 'rent_flats',
            'show_management_panel': request.user.id == int(user_id),
            'user_id': user_id,
        },
    )

def rentflat_detail(request, id):
    flat = get_object_or_404(RentFlat, pk=id)
    dispatcher = LocationDispatcher(deal_type='rent', location=flat.location)
    # TODO check if dispatcher has wrong location
    
    return direct_to_template(
        request,
        template = dispatcher.detail_template,
        extra_context = {
            'object': flat,
            'show_object_controls': flat.can_edit(request.user),
        }
    )


@login_required
def rentflat_new(request, location):
    form_dispatcher = LocationDispatcher(deal_type='rent', location=location)
    if not form_dispatcher.location_valid():
        return redirect(rentflat_new, location='moscow')
    
    if request.method == 'POST':
        instance = RentFlat(owner=request.user, **form_dispatcher.instance_params)
        form = form_dispatcher.form_class(request.POST, instance=instance)
        if form.is_valid():
            flat = form.save()
            
            return redirect_to(request, url=flat.get_absolute_url(), permanent=False)
    else:
        form = form_dispatcher.form_class()
    return direct_to_template(
        request,
        template = "buildings/flat_form.html",
        extra_context = {
            'form': form,
            'locations': form_dispatcher.localized_titles('ru'),
            'location': location,
            'deal_type': 'rent',
        }
    )

@login_required
def rentflat_edit(request, id):
    # get object
    flat = get_object_or_404(RentFlat, pk=id)
    
    if not flat.can_edit(request.user):
        raise Http404
    
    # get form
    form_dispatcher = LocationDispatcher(deal_type='rent', location=flat.location)
    # TODO check is form_dispatcher has wrong location
    # if not form_dispatcher.location_valid():
    #     raise
    
    # process form
    if request.method == 'POST':
        form = form_dispatcher.form_class(request.POST, instance=flat)
        if form.is_valid():
            form.save()
            return redirect_to(
                request,
                url=flat.get_absolute_url(),
                permanent=False
            )
    else:
        form = form_dispatcher.form_class(instance=flat)
    return direct_to_template(
        request,
        template = "buildings/flat_form.html",
        extra_context = {'form': form}
    )


# =============
# = SellFlats =
# =============
def user_sellflat_list(request, user_id):
    return object_list(
        request,
        queryset = SellFlat.objects.filter(owner__pk__exact=user_id),
        extra_context = {
            'objects_type': 'sell_flats',
            'show_management_panel': request.user.id == int(user_id),
            'user_id': user_id,
        },
    )

def sellflat_detail(request, id):
    flat = get_object_or_404(SellFlat, pk=id)
    dispatcher = LocationDispatcher(deal_type='sell', location=flat.location)
    # TODO check if dispatcher has wrong location
    
    return direct_to_template(
        request,
        template = dispatcher.detail_template,
        extra_context = {
            'object': flat,
            'show_object_controls': flat.can_edit(request.user),
        }
    )


@login_required
def sellflat_new(request, location):
    form_dispatcher = LocationDispatcher(deal_type='sell', location=location)
    if not form_dispatcher.location_valid():
        return redirect(sellflat_new, location='moscow')
    
    if request.method == 'POST':
        instance = SellFlat(owner=request.user, **form_dispatcher.instance_params)
        form = form_dispatcher.form_class(request.POST, instance=instance)
        if form.is_valid():
            flat = form.save()
            
            return redirect_to(request, url=flat.get_absolute_url(), permanent=False)
    else:
        form = form_dispatcher.form_class()
    return direct_to_template(
        request,
        template = "buildings/flat_form.html",
        extra_context = {
            'form': form,
            'locations': form_dispatcher.localized_titles('ru'),
            'location': location,
            'deal_type': 'sell',
        }
    )

@login_required
def sellflat_edit(request, id):
    # get object
    flat = get_object_or_404(SellFlat, pk=id)
    
    if not flat.can_edit(request.user):
        raise Http404
    
    # get form
    form_dispatcher = LocationDispatcher(deal_type='sell', location=flat.location)
    # TODO check if form_dispatcher has wrong location
    
    # process form
    if request.method == 'POST':
        form = form_dispatcher.form_class(request.POST, instance=flat)
        if form.is_valid():
            form.save()
            return redirect_to(
                request,
                url=flat.get_absolute_url(),
                permanent=False
            )
    else:
        form = form_dispatcher.form_class(instance=flat)
    return direct_to_template(
        request,
        template = "buildings/flat_form.html",
        extra_context = {'form': form}
    )


# ==========
# = Search =
# ==========
def search(request, deal_type, location):
    if request.method != 'GET':
        raise Http404
    form_dispatcher = LocationDispatcher(deal_type=deal_type, location=location)
    
    if request.GET:
        form = form_dispatcher.search_form_class(request.GET)
        if form.is_valid():
            # Perform search actions
            return direct_to_template(
                request,
                template = "buildings/search/results.html",
            )
    else:
        form = form_dispatcher.search_form_class()
    return direct_to_template(
        request,
        template = form_dispatcher.search_form_template,
        extra_context = {
            'form': form,
            'locations': LocationDispatcher.localized_titles('ru'),
            'location': location,
            'deal_types': LocationDispatcher.deal_types(),
            'deal_type': deal_type,
        }
    )

