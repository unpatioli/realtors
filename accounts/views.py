from accounts.forms import RegistrationForm, UserprofileForm
from accounts.models import UserProfile

from django.contrib.auth.decorators import login_required
from django.views.generic.simple import direct_to_template, redirect_to

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
            
            return redirect_to(request, url='/', permanent=False)
    else:
        form = RegistrationForm()
    
    return direct_to_template(
        request,
        template = "accounts/user_form.html",
        extra_context = {'form': form}
    )

def profile(request, user_id):
    if request.user.is_authenticated() and request.user.id == int(user_id):
        return redirect_to(request, url='/accounts/profile/', permanent=False)
    try:
        userprofile = UserProfile.objects.get(user=user_id)
    except UserProfile.DoesNotExist:
        return direct_to_template(
            request,
            template = "accounts/userprofile_not_found.html"
        )
    return direct_to_template(
        request,
        template = "accounts/userprofile.html",
        extra_context = {'userprofile': userprofile, 'is_my_profile': False}
    )

@login_required
def my_profile(request):
    try:
        userprofile = request.user.get_profile()
    except UserProfile.DoesNotExist:
        return redirect_to(request, url="/accounts/profile/new/", permanent=False)
    
    return direct_to_template(
        request,
        template = "accounts/userprofile.html",
        extra_context = {'userprofile': userprofile, 'is_my_profile': True}
    )

@login_required
def my_profile_new(request):
    if request.method == 'POST':
        form = UserprofileForm(request.POST, request.FILES)
        if form.is_valid():
            up = form.save(commit=False)
            up.user = request.user
            up.save()
            
            return redirect_to(request, url=up.get_absolute_url(), permanent=False)
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
        return redirect_to(request, url="/accounts/profile/new/", permanent=False)
    
    if request.method == 'POST':
        form = UserprofileForm(request.POST, request.FILES, instance=userprofile)
        if form.is_valid():
            form.save()
            return redirect_to(
                request,
                url=userprofile.get_absolute_url(),
                permanent=False
            )
    else:
        form = UserprofileForm(instance=userprofile)
    
    return direct_to_template(
        request,
        template = "accounts/userprofile_form.html",
        extra_context = {'form': form}
    )
