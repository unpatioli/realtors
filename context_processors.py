from django.conf import settings

def inbox_not_read_count(request):
    res = {}
    if request.user.is_authenticated():
        res = {
            'inbox_not_read_count': request.user.inbox.filter(is_draft = False, recipient_deleted_at__isnull = True, is_read = False).count(),
        }
    return res
