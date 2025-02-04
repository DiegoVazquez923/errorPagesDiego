from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
import re
class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['email', 'name', 'surname', 'control_number', 'age', 'tel',
    'password1', 'password2']
    widgets = {
            'email': forms.EmailInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Correo electrónico',
                    'required': True,
                    'pattern': r'^[a-zA-Z0-9]+@utez\.edu\.mx$',
                    'title': 'Debe ingresar un correo institucional que termine en @utez.edu.mx'
                }
            ),
            'name': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Nombre',
                    'required': True,
                    'pattern': r'^[A-Za-z]+$',
                    'title': 'Solo se permiten letras y espacios'
                }
            ),
            'surname': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Apellido',
                    'required': True,
                    'pattern': r'^[A-Za-z]+$',
                    'title': 'Solo se permiten letras y espacios'
                }
            ),
            'control_number': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Número de control',
                    'required': True,
                    'pattern': r'^\d{5}[A-Za-z]{2}\d{3}$',
                    'title': 'Debe tener 5 números, seguidos de 2 letras y luego 3 números (Ejemplo: 12345AB678)'
                }
            ),
            'age': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Edad',
                    'required': True,
                    'min': 10,
                    'max': 99,
                    'title': 'Ingrese su edad'
                }
            ),
            'tel': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Teléfono',
                    'required': True,
                    'pattern': r'^\d{10}$',
                    'title': 'Debe contener exactamente 10 dígitos'
                }
            ),
            'password1': forms.PasswordInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Contraseña',
                    'required': True,
                    'minlength': 8,
                    'pattern': r'^(?=.*\d)(?=.*[!#$%&?]).{8,}$',
                    'title': 'Debe contener al menos 8 caracteres'
                }
            ),
            'password2': forms.PasswordInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Confirmar Contraseña',
                    'required': True,
                    'minlength': 8,
                    'pattern': r'^(?=.*\d)(?=.*[!#$%&?]).{8,}$',
                    'title': 'Debe coincidir con la contraseña ingresada'
                }
            ),
        }


class CustomUserLoginForm(AuthenticationForm):
    pass

class CustomLoginForm(AuthenticationForm):
    email = forms.CharField(label="Correo electrónico", max_length=150)
    password = forms.CharField(label="Contraseña", widget=forms.PasswordInput)
    password1 = forms.CharField(label="Contraseña", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Confirmar contraseña", widget=forms.PasswordInput)
    matricula = forms.CharField(label="Matrícula", max_length=10, min_length=10)

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get("username")
        password = cleaned_data.get("password")
        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise forms.ValidationError("Usuario o contraseña incorrectos.")

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if not re.match(r"^[a-zA-Z0-9._%+-]+@utez\.edu\.mx$", email):
            raise forms.ValidationError("El correo debe ser institucional de la UTEZ (@utez.edu.mx).")
        return email

    def clean_password1(self):
        password = self.cleaned_data.get("password1")
        if len(password) < 8:
            raise forms.ValidationError("La contraseña debe tener al menos 8 caracteres.")
        if not re.search(r"\d", password):
            raise forms.ValidationError("La contraseña debe contener al menos un número.")
        if not re.search(r"[!#$%&?]", password):
            raise forms.ValidationError("La contraseña debe contener al menos un símbolo (!, #, $, %, & o ?).")
        return password

    def clean_matricula(self):
        matricula = self.cleaned_data.get("matricula")
        if not re.match(r"^\d{5}[A-Za-z]{2}\d{3}$", matricula):
            raise forms.ValidationError("La matrícula debe tener 10 caracteres y seguir el formato correcto.")
        return matricula

        return cleaned_data