from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from .models import Product


class UpdateUserForm(forms.ModelForm):
    age = forms.IntegerField()  # можно указать для стандартной валидации min_value=18
    username = forms.CharField(
        min_length=4,
        max_length=15,
        help_text='Обязательное поле, не более 15 символов',
    )

    def clean_age(self):
        """validate age field"""
        value = self.cleaned_data['age']
        if value < 18:
            raise ValidationError('Возраст должен быть больше 18 лет')
        return value

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')


class ProductAddForm(forms.ModelForm):

    class Meta:
        model = Product
        fields = ('name', 'description', 'category', 'price', 'tags')
