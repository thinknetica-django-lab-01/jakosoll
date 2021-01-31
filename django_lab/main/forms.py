from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User


class UpdateUserForm(forms.ModelForm):
    age = forms.IntegerField()  # можно указать для стандартной валидации min_value=18

    def clean_age(self):
        """validate age field"""
        value = self.cleaned_data['age']
        if value < 18:
            raise ValidationError('Возраст должен быть больше 18 лет')
        return value

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')


