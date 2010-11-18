from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.views.generic.simple import direct_to_template
from django.http import Http404

from images.models import ImagedItem
from images.forms import ImageForm

# ==========
# = Images =
# ==========
def object_image_list(request, content_type, object_id):
    try:
        obj = ContentType.objects.get(model=content_type).get_object_for_this_type(pk=object_id)
    except:
        raise Http404
    
    return direct_to_template(
        request,
        template = "images/object_list.html",
        extra_context = {
            'object': obj,
            'images': obj.images.all(),
            'show_object_controls': obj.can_edit(request.user),
            
            'content_type': content_type,
            'object_id': object_id,
        }
    )

@login_required
def object_image_new(request, content_type, object_id):
    try:
        obj = ContentType.objects.get(model=content_type).get_object_for_this_type(pk=object_id)
        if not obj.can_edit(request.user):
            raise Http404
    except:
        raise Http404
    
    if request.method == "POST":
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            i = form.save(commit = False)
            i.content_object = obj
            i.save()
            return redirect(object_image_list, content_type=content_type, object_id=object_id)
    else:
        form = ImageForm()
    return direct_to_template(
        request,
        template = "images/object_form.html",
        extra_context = {
            'form': form,
            
            'content_type': content_type,
            'object_id': object_id
        }
    )

@login_required
def object_image_edit(request, content_type, object_id, id):
    try:
        obj = ContentType.objects.get(model=content_type).get_object_for_this_type(pk=object_id)
        if not obj.can_edit(request.user):
            raise Http404
        img = obj.images.get(pk=id)
    except:
        raise Http404
    
    if request.method == "POST":
        form = ImageForm(request.POST, request.FILES, instance = img)
        if form.is_valid():
            form.save()
            return redirect(object_image_list, content_type=content_type, object_id=object_id)
    else:
        form = ImageForm(instance = img)
    return direct_to_template(
        request,
        template = "images/object_form.html",
        extra_context = {
            'form': form,
            
            'content_type': content_type,
            'object_id': object_id
        }
    )

