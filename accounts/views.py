from accounts.forms import RegistrationForm, UserprofileForm, RealtorForm
from accounts.models import UserProfile, Realtor

from django.contrib.auth.decorators import login_required
from django.views.generic.simple import direct_to_template
from django.shortcuts import redirect, get_object_or_404

def register(request):
    from django.contrib.auth.models import User
    
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                username = form.cleaned_data["username"],
                email = form.cleaned_data["email"],
                password = form.cleaned_data["password"]
            )
            user.first_name = form.cleaned_data["first_name"]
            user.last_name = form.cleaned_data["last_name"]
            user.save()
            
            return redirect('/')
    else:
        form = RegistrationForm()
    
    return direct_to_template(
        request,
        template = "accounts/user_form.html",
        extra_context = {'form': form}
    )

def profile(request, user_id):
    if request.user.is_authenticated() and request.user.id == int(user_id):
        return redirect(my_profile)
    userprofile = get_object_or_404(UserProfile, user=user_id)
    if not userprofile.can_show():
        return direct_to_template(
            request,
            template = "accounts/closed_profile.html",
        )
    return direct_to_template(
        request,
        template = "accounts/userprofile.html",
        extra_context = {
            'userprofile': userprofile,
            'is_my_profile': False
        }
    )

@login_required
def my_profile(request):
    try:
        userprofile = request.user.get_profile()
    except UserProfile.DoesNotExist:
        return redirect(my_profile_new)
    
    return direct_to_template(
        request,
        template = "accounts/userprofile_authenticated.html",
        extra_context = {'userprofile': userprofile}
    )

@login_required
def my_profile_new(request):
    if request.user.userprofile_set.exists():
        return redirect(my_profile_edit)
    if request.method == 'POST':
        form = UserprofileForm(request.POST, request.FILES)
        if form.is_valid():
            up = form.save(commit=False)
            up.user = request.user
            up.save()
            
            return redirect(up)
    else:
        form = UserprofileForm()
    
    return direct_to_template(
        request,
        template = "accounts/userprofile_form.html",
        extra_context = {'form': form}
    )

@login_required
def my_profile_edit(request):
    try:
        userprofile = request.user.get_profile()
    except UserProfile.DoesNotExist:
        return redirect(my_profile_new)
    
    if request.method == 'POST':
        form = UserprofileForm(request.POST, request.FILES, instance=userprofile)
        if form.is_valid():
            form.save()
            return redirect(userprofile)
    else:
        form = UserprofileForm(instance=userprofile)
    
    return direct_to_template(
        request,
        template = "accounts/userprofile_form.html",
        extra_context = {'form': form}
    )

@login_required
def realtor_new(request):
    if request.user.realtor_set.exists():
        return redirect(realtor_edit)
    if request.method == 'POST':
        form = RealtorForm(request.POST)
        if form.is_valid():
            r = form.save(commit=False)
            r.user = request.user
            r.save()
            
            return redirect(r)
    else:
        form = RealtorForm()
    
    return direct_to_template(
        request,
        template = "accounts/realtor_form.html",
        extra_context = {'form': form}
    )

@login_required
def realtor_edit(request):
    try:
        realtor = request.user.realtor_set.get()
    except Realtor.DoesNotExist:
        return redirect(realtor_new)
    
    if request.method == 'POST':
        form = RealtorForm(request.POST, instance=realtor)
        if form.is_valid():
            form.save()
            return redirect(realtor)
    else:
        form = RealtorForm(instance=realtor)
    
    return direct_to_template(
        request,
        template = "accounts/realtor_form.html",
        extra_context = {'form': form}
    )

