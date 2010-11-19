# -*- coding:utf-8 -*-
from django import forms
from django.contrib.auth.models import User
from accounts.models import UserProfile, Realtor, Agency

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
        from form_utils.widgets import CalendarWidget
        
        model = UserProfile
        fields = ('birthday', 'gender', 'is_closed', 'avatar', 'description')
        widgets = {
            'birthday': CalendarWidget,
        }
    

class RealtorForm(forms.ModelForm):
    from form_utils.widgets import DivCheckboxSelectMultiple
    
    agencies = forms.ModelMultipleChoiceField(
                                label=u"Агентство",
                                help_text=u"Если вашего агентства нет в списке, вы можете его <a href=\"/accounts/agency/new\">добавить</a>",
                                queryset=Agency.moderated_objects.all(),
                                widget=DivCheckboxSelectMultiple(classes=['scroll'])
                            )
    
    class Meta:
        model = Realtor
        fields = ('experience', 'agencies', 'is_private', 'in_sales', 'in_rents', 'in_camps', 'in_commercials', 'in_msk', 'in_msk_region', 'commission_from', 'commission_to', 'deal_commission', 'phone', 'description')
    

class AgencyFormBase(forms.ModelForm):
    class Meta:
        model = Agency
    

class AgencyForm(AgencyFormBase):
    class Meta(AgencyFormBase.Meta):
        exclude = ('administrators', 'is_moderated',)
