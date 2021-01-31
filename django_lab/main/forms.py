from django.forms import ModelForm
from django import forms
from .models import Product
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User


class UpdateUserForm(ModelForm):

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')


class ProductAddForm(forms.ModelForm):

    class Meta:
        model = Product
        fields = ('name', 'description', 'category', 'price', 'tags')


