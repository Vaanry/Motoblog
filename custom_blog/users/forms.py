from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.db import models
from django.core.exceptions import ValidationError
from .validators import correct_username

User = get_user_model()


class CustomUserCreationForm(UserCreationForm):
    username = models.CharField('Имя пользователя', max_length=20,
                                validators=(correct_username,))

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def clean_username(self):
        username = self.cleaned_data.get("username")
        if correct_username(username):
            raise ValidationError(
                'Имя пользователя должно состоять из букв латинского алфавита,\
                цифр и символов @/./+/-/_.'
            )
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Username is not unique")
        return username

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email is not unique")
        return email


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'foto', 'bio', 'motobike')

    def clean_username(self):
        current_username = self.get_initial_for_field(self.fields['username'], 'username')
        username = self.cleaned_data.get("username")
        if correct_username(username):
            raise ValidationError(
                'Имя пользователя должно состоять из букв латинского алфавита,\
                цифр и символов @/./+/-/_.'
            )
        if current_username!=username and User.objects.filter(username=username).exists():
            raise forms.ValidationError("Пользователь с таким username уже существует")
        return username

    def clean_email(self):
        current_email = self.get_initial_for_field(self.fields['email'], 'email')
        email = self.cleaned_data.get("email")
        if email != current_email and User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email адрес должен быть уникальным")
        return email
