from app.models import Customer
from django import forms
from django.contrib.auth import password_validation
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm,UsernameField,PasswordChangeForm,PasswordResetForm,SetPasswordForm
from django.contrib.auth.password_validation import password_changed, password_validators_help_text_html 
from django.forms import widgets
from django.utils.translation import gettext,gettext_lazy as _

class RegistrationForm(UserCreationForm):
    username = forms.CharField(required=True,label='Username',widget=forms.TextInput(attrs={'class':'form-control'}))
    email = forms.CharField(required=True,label='Email',widget=forms.EmailInput(attrs={'class':'form-control'}))
    password1 = forms.CharField(required=True,label='Password',widget=forms.PasswordInput(attrs={'class':'form-control'}))
    password2 = forms.CharField(required=True,label='Confirm Password',widget=forms.PasswordInput(attrs={'class':'form-control'}))  
    class Meta:
        model = User
        fields = ['username','email','password1','password2']
        
class LoginForm(AuthenticationForm):
    username = UsernameField(widget=forms.TextInput(attrs={'autofocus':True,'class':'form-control'}))
    password = forms.CharField(label=_("Password"),strip=False,widget=forms.PasswordInput(attrs={'autocomplete':'current-password','class':'form-control'}))

class PasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(label='Password',widget=forms.PasswordInput(attrs={'autocomplete':'current-password','autofocus':True,'class':'form-control'}))
    new_password1 = forms.CharField(label='New Passoword',widget=forms.PasswordInput(attrs={'autocomplete':'new-password','class':'form-control'}),help_text=password_validation.password_validators_help_text_html())
    new_password2 = forms.CharField(label='Confirm New password',strip=False,widget=forms.PasswordInput(attrs={'class':'form-control'}))

class PasswordResetForm(PasswordResetForm):
    email = forms.EmailField(label='Email',widget=forms.EmailInput(attrs={'autocomplete':'email','class':'form-control'}))

class SetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(label='New Passoword',widget=forms.PasswordInput(attrs={'autocomplete':'new-password','class':'form-control'}),help_text=password_validation.password_validators_help_text_html())
    new_password2 = forms.CharField(label='Confirm New password',strip=False,widget=forms.PasswordInput(attrs={'class':'form-control'}))

class CustomerProfileForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['name','locality','city','state','zipcode']
        widgets = {
            'name' : forms.TextInput(attrs={'class':'form-control'}),
            'locality' : forms.TextInput(attrs={'class':'form-control'}),
            'city' : forms.TextInput(attrs={'class':'form-control'}),
            'state' : forms.Select(attrs={'class':'form-control'}),
            'zipcode' : forms.NumberInput(attrs={'class':'form-control'}),
        }
