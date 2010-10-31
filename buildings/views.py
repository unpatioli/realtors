# -*- coding:utf-8 -*-
from buildings.models import RentFlat, SellFlat
from buildings.form_dispatcher import FormDispatcher

from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views.generic.simple import direct_to_template, redirect_to
from django.views.generic.list_detail import object_list, object_detail


def user_rentflat_list(request, user_id):
    return object_list(
        request,
        queryset = RentFlat.objects.filter(owner__pk__exact=user_id),
        template_object_name = 'flat',
        extra_context = {'show_management_panel': request.user.id == int(user_id)},
    )

def rentflat_detail(request, id):
    return object_detail(
        request,
        queryset = RentFlat.objects.all(),
        object_id = id,
        template_object_name = 'flat'
    )


@login_required
def rentflat_new(request, location):
    form_dispatcher = FormDispatcher(deal_type='rent', location=location)
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
        template = "buildings/rentflat_form.html",
        extra_context = {'form': form}
    )

@login_required
def rentflat_edit(request, id):
    # get object
    flat = get_object_or_404(RentFlat, pk=id)
    
    # get form
    form_dispatcher = FormDispatcher(deal_type='rent', location=flat.location)
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
        template = "buildings/rentflat_form.html",
        extra_context = {'form': form}
    )

