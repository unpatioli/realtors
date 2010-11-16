# -*- coding:utf-8 -*-
from django import forms
from accounts.models import UserProfile, Realtor

class RegistrationForm(forms.Form):
    username = forms.CharField(max_length=30, label=u"Имя пользователя")
    password = forms.CharField(max_length=30, widget=forms.PasswordInput(render_value=False), label=u"Пароль")
    password_retype = forms.CharField(max_length=30, widget=forms.PasswordInput(render_value=False), label=u"Пароль еще раз")
    
    email = forms.EmailField(max_length=75, label=u"Электронная почта")
    
    first_name = forms.CharField(max_length=30, required=False, label=u"Имя")
    last_name = forms.CharField(max_length=30, required=False, label=u"Фамилия")
    
    # =========================
    # = Form-wide validations =
    # =========================
    def clean_password_retype(self):
        password = self.cleaned_data['password']
        password_retype = self.cleaned_data['password_retype']
        if password_retype != password:
            raise forms.ValidationError(u"Пароли не совпадают")
        return password_retype
    
    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username):
            raise forms.ValidationError(u"Это имя уже занято")
        return username
    
    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email):
            raise forms.ValidationError(u"Такой email уже зарегистрирован")
        return email
    

class UserprofileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('birthday', 'gender', 'is_closed', 'avatar', 'description')
    

class RealtorForm(forms.ModelForm):
    class Meta:
        model = Realtor
        # fields = ('')
        exclude = ('user',)