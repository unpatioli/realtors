import datetime
import operator

from django.db.models import Q, F

from buildings.models import RentFlat, SellFlat


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
    return reduce(operator.and_, arr)


# =========================
# = Common find functions =
# =========================
def __building_find(form):
    q_period = Q()
    period = int(form.cleaned_data.get('period'))
    if period:
        today = datetime.date.today()
        delta = datetime.timedelta(days=period)
        q_period = Q(created_at__gte = today - delta)
    
    q_price_currency = q_gt_lt(form, 'price')
    if len(q_price_currency.children):
        q_price_currency = q_price_currency & q(form, 'currency')
    q_arr = [
        q_price_currency,
        q(  form,
            'with_photo',
            model_field_name = 'images',
            query_type = 'isnull',
            negative = True
        ),
        q_period,
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
        
        q(form, 'furniture'),
        balcony_q,
        q(form, 'fridge'),
        q(form, 'wash_machine'),
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
    zero_commission_q = Q()
    if form.cleaned_data.get('zero_commission'):
        zero_commission_q = Q(owner__realtor__commission_from = 0) & Q(owner__realtor__commission_to = 0)
    q_arr = [
        q(form, 'payment_period'),
        
        q(form, 'pets'),
        q(form, 'children'),
        
        q(form, 'agency', model_field_name='owner__realtor__agency_title') | q(form, 'owner__realtor__private'),
        zero_commission_q
    ]
    return q_arr

def __sell_flat_find(form):
    q_arr = [
        q(form, 'mortgage'),
        q(part_in_flat, 'part_in_flat'),
    ]
    return q_arr




# ========
# = Rent =
# ========
def moscow_rentflat_find(form):
    q_arr = __moscow_flat_find(form) + __rent_flat_find(form)
    return RentFlat.moscow_objects.filter(reduce_and(q_arr))

def moscow_region_rentflat_find(form):
    q_arr = __moscow_region_flat_find(form) + __rent_flat_find(form)
    return RentFlat.moscow_region_objects.filter(reduce_and(q_arr))

def common_rentflat_find(form):
    q_arr = __common_flat_find(form) + __rent_flat_find(form)
    return RentFlat.common_objects.filter(reduce_and(q_arr))

# ========
# = Sell =
# ========
def moscow_sellflat_find(form):
    q_arr = __moscow_flat_find(form) + __sell_flat_find(form)
    return SellFlat.moscow_objects.filter(reduce_and(q_arr))
    
def moscow_region_sellflat_find(form):
    q_arr = __moscow_region_flat_find(form) + __sell_flat_find(form)
    return SellFlat.moscow_region_objects.filter(reduce_and(q_arr))

def common_sellflat_find(form):
    q_arr = __common_flat_find(form) + __sell_flat_find(form)
    return SellFlat.common_objects.filter(reduce_and(q_arr))

