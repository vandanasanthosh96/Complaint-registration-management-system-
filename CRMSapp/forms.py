from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class PublicUserCreationForm(UserCreationForm):
    email=forms.EmailField(required=True)
    name=forms.CharField(max_length=30)
    idproof=forms.CharField(max_length=15)
    address =forms.CharField(max_length=40)
    mobile = forms.CharField(max_length=12)

    class Meta:
        model=User
        fields = ('username', 'email', 'password1', 'password2', 'name', 'idproof', 'address', 'mobile')