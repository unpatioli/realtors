from django.contrib import auth
from django.views.generic.simple import direct_to_template, redirect_to
from django import http

from accounts.forms import AuthForm

def login(request):
    if request.user.is_authenticated():
        return redirect_to(request, url='/')
    
    if request.method == 'POST':
        form = AuthForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            
            user = auth.authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    auth.login(request, user)
                    return redirect_to(request, url='/')
                else:
                    # TODO Disabled account error message
                    return http.HttpResponseNotFound("Disabled account error message")
            else:
                # TODO Invalid login error message
                # return http.HttpResponseNotFound("Invalid login error message")
                form = AuthForm()
    else:
        form = AuthForm()
    
    return direct_to_template(
        request,
        template = 'accounts/login.html',
        extra_context = { 'form': form }
    )

def logout(request):
    auth.logout(request)
    return redirect_to(request, url='/')

