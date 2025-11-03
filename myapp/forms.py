from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Reservacion

class RegistroForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={
        'placeholder': 'Correo electrónico',
    }))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']




class ReservacionForm(forms.ModelForm):
    class Meta:
        model = Reservacion
        fields = ['salon', 'fecha_reserva']  
        widgets = {
            'fecha_reserva': forms.DateInput(
                attrs={
                    'type': 'date',
                    'id': 'fecha_reserva',
                    'autocomplete': 'off',
                    'class': 'w-full border border-gray-300 rounded-md px-3 py-2',
                    'placeholder': 'Selecciona la fecha de la reserva'
                }
            )
        }