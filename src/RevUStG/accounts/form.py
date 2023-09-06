from typing import Any, Dict
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import*

class RegisterForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={"placeholder":"Username"}))
    email = forms.CharField(widget=forms.EmailInput(attrs={"placeholder":"Email"}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder":"Password"}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder":"Re-enter password"}))


    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def clean(self) -> Dict[str, Any]:
        return super().clean()


class CustomerUpdateForm(ModelForm):
    class Meta:
        model = Customer
        fields = '__all__'
        exclude = ['user', 'coins', 'profile_image']

    def clean(self) -> Dict[str, Any]:
        return super().clean()

class PhoneCardForm(ModelForm):
    class Meta:
        model = PhoneCardPayment
        fields = '__all__'
        exclude = ['id']
    def clean(self) -> Dict[str, Any]:
        return super().clean()
    
class BankAccountForm(ModelForm):
    class Meta:
        model = BankAccountPayment
        fields = '__all__'
        exclude = ['id']
    def clean(self) -> Dict[str, Any]:
        return super().clean()