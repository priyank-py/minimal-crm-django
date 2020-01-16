from django import forms
from django.contrib.auth.models import User
from .models import Employee

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = '__all__'

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = '__all__'
        exclude = ('user',)