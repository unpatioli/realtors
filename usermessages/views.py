from django.contrib.auth.decorators import login_required

@login_required
def message_list(request, box_type='inbox'):
    raise NotImplementedError

@login_required
def message_new(request):
    raise NotImplementedError

@login_required
def message_edit(request, object_id):
    raise NotImplementedError

@login_required
def message_delete(request, object_id):
    raise NotImplementedError

