# -*- coding:utf-8 -*-
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from django.http import Http404
from django.views.generic.simple import direct_to_template
from django.views.generic.list_detail import object_list
from django.core.urlresolvers import reverse

from django.contrib.auth.models import User
from usermessages.models import Usermessage
from usermessages.forms import UsermessageForm

@login_required
def inbox(request):
    return object_list(
        request,
        queryset = request.user.inbox.filter(is_draft = False, recipient_deleted_at__isnull = True),
        extra_context = {'box_type': 'inbox'}
    )

@login_required
def outbox(request):
    return object_list(
        request,
        queryset = request.user.outbox.filter(is_draft = False, sender_deleted_at__isnull = True),
        extra_context = {'box_type': 'outbox'}
    )

@login_required
def drafts(request):
    return object_list(
        request,
        queryset = request.user.outbox.filter(is_draft = True, sender_deleted_at__isnull = True),
        extra_context = {'box_type': 'drafts'}
    )

@login_required
def trash(request):
    from django.db.models import Q
    
    q = Q(sender = request.user, sender_deleted_at__isnull = False, sender_deleted_permanent = False) | Q(recipient =request.user, recipient_deleted_at__isnull = False, recipient_deleted_permanent = False)
    return object_list(
        request,
        queryset = Usermessage.objects.filter(q),
        extra_context = {'box_type': 'trash'}
    )

@login_required
def message_new(request, user_id):
    recipient = get_object_or_404(User, pk=user_id)
    if request.method == "POST":
        form = UsermessageForm(request.POST)
        if form.is_valid():
            usermessage = form.save(commit=False)
            usermessage.sender = request.user
            usermessage.recipient = recipient
            usermessage.save()
            if usermessage.is_draft:
                messages.success(request, u"Сообщение сохранено в черновиках")
                return redirect(drafts)
            messages.success(request, u"Сообщение отправлено")
            return redirect(inbox)
        else:
            messages.error(request, u"Сообщение не отправлено")
    else:
        form = UsermessageForm()
    return direct_to_template(
        request,
        template = "usermessages/compose_form.html",
        extra_context = {
            'form': form,
            'recipient': recipient,
        }
    )

@login_required
def message_send(request, object_id):
    usermessage = get_object_or_404(Usermessage, pk=object_id)
    if usermessage.sender != request.user or not usermessage.is_draft:
        raise Http404
    if request.method == "POST":
        usermessage.is_draft = False
        usermessage.save()
        messages.success(request, u"Сообщение отправлено")
        return redirect(outbox)
    return direct_to_template(
        request,
        template = "usermessages/usermessage_confirm_send.html",
        extra_context = {'usermessage': usermessage}
    )

@login_required
def message_show(request, object_id):
    usermessage = get_object_or_404(Usermessage, pk=object_id)
    if usermessage.sender != request.user and usermessage.recipient != request.user:
        raise Http404
    if usermessage.sender == request.user and usermessage.sender_deleted_permanent:
        raise Http404
    if usermessage.recipient == request.user:
        if usermessage.recipient_deleted_permanent:
            raise Http404
        if not usermessage.is_draft and not usermessage.is_read:
            usermessage.is_read = True
            usermessage.save()
    return direct_to_template(
        request,
        template = "usermessages/usermessage.html",
        extra_context = {
            'usermessage': usermessage,
            'show_edit_send': usermessage.is_draft,
        }
    )

@login_required
def message_edit(request, object_id):
    usermessage = get_object_or_404(Usermessage, pk=object_id)
    if usermessage.sender != request.user or not usermessage.is_draft or usermessage.sender_deleted_at is not None:
        raise Http404
    if request.method == "POST":
        form = UsermessageForm(request.POST, instance=usermessage)
        if form.is_valid():
            form.save()
            messages.success(request, u"Сообщение изменено")
            return redirect(drafts)
        else:
            messages.error(request, u"Сообщение не изменено")
    else:
        form = UsermessageForm(instance=usermessage)
    return direct_to_template(
        request,
        template = "usermessages/compose_form.html",
        extra_context = {'form': form},
    )

@login_required
def message_delete(request, object_id):
    from datetime import datetime
    
    usermessage = get_object_or_404(Usermessage, pk=object_id)
    if usermessage.sender == request.user:
        is_permanent = usermessage.sender_deleted_at is not None
        if request.method == "POST":
            if is_permanent:
                usermessage.sender_deleted_permanent = True
                usermessage.save()
                messages.success(request, u"Сообщение удалено")
                return redirect(trash)
            else:
                usermessage.sender_deleted_at = datetime.today()
                usermessage.save()
                messages.success(request, u"Сообщение отправлено в корзину")
                if usermessage.is_draft:
                    return redirect(drafts)
                return redirect(outbox)
    elif usermessage.recipient == request.user:
        is_permanent = usermessage.recipient_deleted_at is not None
        if request.method == "POST":
            if is_permanent:
                usermessage.recipient_deleted_permanent = True
                usermessage.save()
                messages.success(request, u"Сообщение удалено")
                return redirect(trash)
            else:
                usermessage.recipient_deleted_at = datetime.today()
                usermessage.save()
                messages.success(request, u"Сообщение отправлено в корзину")
                return redirect(inbox)
    else:
        raise Http404
    return direct_to_template(
        request,
        template = "usermessages/usermessage_confirm_delete.html",
        extra_context = {
            'is_permanent': is_permanent,
            'usermessage': usermessage,
        },
    )

