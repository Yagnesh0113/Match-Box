from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm
from django import forms

class UserPasswordResetForm(PasswordResetForm):
    def __init__(self, *args, **kwargs):
        super(UserPasswordResetForm, self).__init__(*args, **kwargs)

    email = forms.EmailField(label='', widget=forms.EmailInput(attrs={
        'class': 'form-control border-left-0',
        'placeholder': 'Enter your email',
        'type': 'email',
        'name': 'email'
        }))

class UserPasswordResetconfirmForm(SetPasswordForm):
    def __init__(self, *args, **kwargs):
        super(UserPasswordResetconfirmForm, self).__init__(*args, **kwargs)

    new_password1 = forms.CharField(label='', widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter your New PassWord',
        'type': 'password',
        'name': 'New Password'
        }))
    
    new_password2 = forms.CharField(label='', widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter your Confirm Password',
        'type': 'password',
        'name': 'Confirm Password'
        }))