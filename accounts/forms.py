# -*- coding:utf-8 -*-
from django import forms

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
    

