from django.db.models import Q, F

from buildings.models import RentFlat, SellFlat


# =========================
# = Common find functions =
# =========================
def __building_find(form):
    import datetime
    
    q_period = Q()
    period = form.cleaned_data.get('period')
    if period:
        today = datetime.date.today()
        delta = datetime.timedelta(days=period)
        q_period = Q(created_at__gte = today - delta)
    
    with_photo_q = Q()
    if form.cleaned_data.get('with_photo'):
        with_photo_q = Q(images__isnull = False)
    
    extra_parameters_q = Q()
    extra_parameters = form.cleaned_data.get('extra_parameters', [])
    if len(extra_parameters):
        extra_parameters_q_arr = [Q(extra_parameters = parameter) for parameter in extra_parameters]
        extra_parameters_q = reduce_and(extra_parameters_q_arr)
    q_arr = [
        with_photo_q,
        q_period,
        extra_parameters_q
    ]
    return q_arr

def __flat_find(form):
    q_floor_no_first = Q()
    floor_no_first = form.cleaned_data.get('floor_no_first')
    if floor_no_first:
        q_floor_no_first = ~Q(floor__exact = 1)
    
    q_floor_no_last = Q()
    floor_no_last = form.cleaned_data.get('floor_no_last')
    if floor_no_last:
        q_floor_no_last = ~Q(floor__exact = F('floors_count'))
    
    balcony_q = Q()
    if form.cleaned_data.get('balcony'):
        balcony_q = Q(balcony_count__gt = 0)
    q_arr = __building_find(form) + [
        q(form, 'rooms_count', query_type='in'),
        q_gt_lt(form, 'total_area'),
        q_gt_lt(form, 'kitchen_area'),
        q_gt_lt(form, 'floor'),
        q_floor_no_first,
        q_floor_no_last,
        q(form, 'house_type'),
        q(form, 'renovation_type'),
        balcony_q,
        
        # q(form, 'furniture'),
        # q(form, 'fridge'),
        # q(form, 'wash_machine'),
    ]
    return q_arr

# ===============
# = By location =
# ===============
def __moscow_flat_find(form):
    q_metro_remoteness_by_legs = Q()
    metro_remoteness_by_legs = int(form.cleaned_data.get('metro_remoteness_by_legs', 0))
    if metro_remoteness_by_legs != 0:
        q_metro_remoteness_by_legs = Q(metro_remoteness_by_legs__lte = metro_remoteness_by_legs)
    
    q_metro_remoteness_by_bus = Q()
    metro_remoteness_by_bus = int(form.cleaned_data.get('metro_remoteness_by_bus', 0))
    if metro_remoteness_by_bus != 0:
        q_metro_remoteness_by_bus = Q(metro_remoteness_by_bus__lte = metro_remoteness_by_bus)
    
    q_arr = __flat_find(form) + [
        q_metro_remoteness_by_legs | q_metro_remoteness_by_bus,
        
        q(form, 'nearest_metro_stations', query_type = 'in'),
    ]
    return q_arr

def __moscow_region_flat_find(form):
    q_mkad_remoteness = Q()
    mkad_remoteness = int(form.cleaned_data.get('mkad_remoteness', 0))
    if mkad_remoteness != 0:
        q_mkad_remoteness = Q(mkad_remoteness__lte = mkad_remoteness)
    
    q_arr = __flat_find(form) + [
        q(form, 'town'),
        q_mkad_remoteness,
    ]
    return q_arr

def __common_flat_find(form):
    q_arr = __flat_find(form) + [
        q(form, 'town'),
    ]
    return q_arr

# ================
# = By deal type =
# ================
def __rent_flat_find(form):
    agency_q = Q()
    if form.cleaned_data.get('agency'):
        agency_q = Q(owner__realtor__agencies__isnull = False)
    zero_commission_q = Q()
    if form.cleaned_data.get('zero_commission'):
        zero_commission_q = Q(owner__realtor__commission_from = 0) & Q(owner__realtor__commission_to = 0)
    
    q_price_arr = []
    payment_period = form.cleaned_data.get('payment_period', 31)
    price_gt = form.cleaned_data.get('price_gt')
    price_lt = form.cleaned_data.get('price_lt')
    if price_gt or price_lt:
        rate = form.cleaned_data.get('currency').rate
        if price_gt:
            price_gt = int(price_gt) / int(rate) / payment_period
            q_price_arr.append(Q(price_EUR__gte = price_gt))
        if price_lt:
            price_lt = int(price_lt) / int(rate) / payment_period
            q_price_arr.append(Q(price_EUR__lte = price_lt))
    q_price = reduce_and(q_price_arr)
    
    q_arr = [
        q_price,
        # q(form, 'payment_period'),
        
        # q(form, 'pets'),
        # q(form, 'children'),
        
        agency_q | q(form, 'private', model_field_name='owner__realtor__is_private'),
        zero_commission_q
    ]
    return q_arr

def __sell_flat_find(form):
    
    q_price_arr = []
    price_gt = form.cleaned_data.get('price_gt')
    price_lt = form.cleaned_data.get('price_lt')
    if price_gt or price_lt:
        rate = form.cleaned_data.get('currency').rate
        if price_gt:
            price_gt = int(price_gt) / int(rate)
            q_price_arr.append(Q(price_EUR__gte = price_gt))
        if price_lt:
            price_lt = int(price_lt) / int(rate)
            q_price_arr.append(Q(price_EUR__lte = price_lt))
    q_price = reduce_and(q_price_arr)
    
    
    q_arr = [
        q_price,
        q(form, 'mortgage'),
        q(form, 'part_in_flat'),
    ]
    return q_arr



# ========
# = Util =
# ========
def q_gt_lt(form, form_field_name, **kwargs):
    import operator
    
    model_field_name = kwargs.get('model_field_name', form_field_name)
    
    name_gt = '%s_gt' % form_field_name
    q_arr = []
    value_gt = form.cleaned_data.get(name_gt)
    if value_gt:
        q_arr.append( Q(**{'%s__gte' % model_field_name: value_gt}) )
        
    name_lt = '%s_lt' % form_field_name
    value_lt = form.cleaned_data.get(name_lt)
    if value_lt:
        q_arr.append( Q(**{'%s__lte' % model_field_name: value_lt}) )
        
    if not len(q_arr):
        return Q()
    return reduce(operator.or_, q_arr)

def q(form, form_field_name, **kwargs):
    model_field_name = kwargs.get('model_field_name', form_field_name)
    query_type = kwargs.get('query_type', 'exact')
    negative = kwargs.get('negative', False)
    
    q = Q()
    value = form.cleaned_data.get(form_field_name)
    if value:
        q = Q(**{'%s__%s' % (model_field_name, query_type): value})
        if negative:
            q = ~q
    return q

def reduce_and(arr):
    import operator
    return reduce(operator.and_, arr, Q())

def post_process(req):
    return req.distinct()


# ========
# = Rent =
# ========
def moscow_rentflat_find(form):
    q_arr = __moscow_flat_find(form) + __rent_flat_find(form)
    return post_process(RentFlat.moscow_objects.filter(reduce_and(q_arr)))

def moscow_region_rentflat_find(form):
    q_arr = __moscow_region_flat_find(form) + __rent_flat_find(form)
    return post_process(RentFlat.moscow_region_objects.filter(reduce_and(q_arr)))

def common_rentflat_find(form):
    q_arr = __common_flat_find(form) + __rent_flat_find(form)
    return post_process(RentFlat.common_objects.filter(reduce_and(q_arr)))

# ========
# = Sell =
# ========
def moscow_sellflat_find(form):
    q_arr = __moscow_flat_find(form) + __sell_flat_find(form)
    return post_process(SellFlat.moscow_objects.filter(reduce_and(q_arr)))

def moscow_region_sellflat_find(form):
    q_arr = __moscow_region_flat_find(form) + __sell_flat_find(form)
    return post_process(SellFlat.moscow_region_objects.filter(reduce_and(q_arr)))

def common_sellflat_find(form):
    q_arr = __common_flat_find(form) + __sell_flat_find(form)
    return post_process(SellFlat.common_objects.filter(reduce_and(q_arr)))

