# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django import forms
from django.contrib.auth.forms import UserCreationForm
from apps.authentication.models import AppUser, UserRole
from utils.validation_messages import ValidationMessages




class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Nombre de usuario",
                "class": "form-control"
            }
        ))
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Contraseña",
                "class": "form-control"
            }
        ))


class SignUpForm(UserCreationForm):
    username = forms.CharField(
        label="Nombre de usuario",
        widget=forms.TextInput(
            attrs={
                "placeholder": "Username",
                "class": "form-control"
            }
        ),
        max_length=150,
        min_length=5
        )
    first_name = forms.CharField(
        label="Nombre",
        widget=forms.TextInput(
            attrs={
                "placeholder": "First Name",
                "class": "form-control"
            }
        ),
        max_length=150,
        min_length=5
    )
    
    last_name = forms.CharField(
        label="Apellido",
        widget=forms.TextInput(
            attrs={
                "placeholder": "Last Name",
                "class": "form-control"
            }
        ),
        max_length=150,
        min_length=5
    )
    role = forms.ModelChoiceField(
        label="Tipo",
        queryset=UserRole.objects.all(),
        widget=forms.Select(
            attrs={
                "class": "form-control"
            }
        )
    )
    email = forms.EmailField(
        label="Correo electrónico",
        widget=forms.EmailInput(
            attrs={
                "placeholder": "Email",
                "class": "form-control"
            }
        ),
        max_length=250,
        min_length=5   
    )
    password1 = forms.CharField(
        label="Contraseña",
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Password",
                "class": "form-control",
                "type": "password"

            }
        ),
        max_length=150,
        min_length=5
    )
    password2 = forms.CharField(
        label="Confirmar contraseña",
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Password check",
                "class": "form-control",
                "type": "password"
            }
        ),
        max_length=150,
        min_length=5
    )

    class Meta:
        model = AppUser
        fields = ('username', 'first_name', 'last_name','email', 'password1', 'password2')
        
class EditUserForm():
    username = forms.CharField(
        label="Nombre de usuario",
        widget=forms.TextInput(
            attrs={
                "placeholder": "Username",
                "class": "form-control"
            }
        ),
        max_length=150,
        min_length=5
        )
    first_name = forms.CharField(
        label="Nombre",
        widget=forms.TextInput(
            attrs={
                "placeholder": "First Name",
                "class": "form-control"
            }
        ),
        max_length=150,
        min_length=5
    )
    
    last_name = forms.CharField(
        label="Apellido",
        widget=forms.TextInput(
            attrs={
                "placeholder": "Last Name",
                "class": "form-control"
            }
        ),
        max_length=150,
        min_length=5
    )
    role = forms.ModelChoiceField(
        label="Tipo",
        queryset=UserRole.objects.all(),
        widget=forms.Select(
            attrs={
                "class": "form-control"
            }
        )
    )
    email = forms.EmailField(
        label="Correo electrónico",
        widget=forms.EmailInput(
            attrs={
                "placeholder": "Email",
                "class": "form-control"
            }
        ),
        max_length=250,
        min_length=5   
    )
    password1 = forms.CharField(
        label="Contraseña",
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Password",
                "class": "form-control",
                "type": "password"

            }
        ),
        max_length=150,
        min_length=5
    )
    password2 = forms.CharField(
        label="Confirmar contraseña",
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Password check",
                "class": "form-control",
                "type": "password"
            }
        ),
        max_length=150,
        min_length=5
    )

    class Meta:
        model = AppUser
        fields = ('username', 'first_name', 'last_name','email', 'password1', 'password2')

ValidationMessages.change_form_error_messages(SignUpForm)