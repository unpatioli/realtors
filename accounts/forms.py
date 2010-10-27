from django import forms

class AuthForm(forms.Form):
    username = forms.CharField(max_length=16)
    password = forms.CharField(max_length=16, widget=forms.PasswordInput(render_value=False))

