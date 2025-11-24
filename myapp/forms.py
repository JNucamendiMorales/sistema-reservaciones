from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Reservacion, Salon

# -----------------------
# 🧩 Formularios para el sitio público
# -----------------------

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

# -----------------------
# ⚙️ Formularios para el panel admin_custom
# -----------------------

class SalonForm(forms.ModelForm):
    class Meta:
        model = Salon
        fields = [
            'nombre',
            'capacidad',
            'descripcion',
            'precio',
            'categoria',
            'ciudad',
            'imagen',
            'disponible',
            'calificacion',  # ✅ Add this line
        ]
        widgets = {
            'descripcion': forms.Textarea(attrs={
                'rows': 3,
                'class': 'form-control',
                'placeholder': 'Describe el salón brevemente...'
            }),
            'precio': forms.NumberInput(attrs={'step': '0.01', 'class': 'form-control'}),
            'capacidad': forms.NumberInput(attrs={'class': 'form-control'}),
            'ciudad': forms.TextInput(attrs={'class': 'form-control'}),
            'categoria': forms.Select(attrs={'class': 'form-control'}),
            'calificacion': forms.NumberInput(attrs={   # ✅ Add this widget too
                'step': '0.1',
                'min': '0',
                'max': '5',
                'class': 'form-control',
                'placeholder': 'Ejemplo: 4.5'
            }),
        }



class ReservacionAdminForm(forms.ModelForm):
    class Meta:
        model = Reservacion
        fields = ['salon', 'usuario', 'fecha_reserva', 'estado', 'pagada', 'precio_total']
        widgets = {
            'fecha_reserva': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'estado': forms.Select(choices=[
                ('pendiente', 'Pendiente'),
                ('confirmada', 'Confirmada'),
                ('cancelada', 'Cancelada'),
            ], attrs={'class': 'form-control'}),
            'precio_total': forms.NumberInput(attrs={'step': '0.01', 'class': 'form-control'}),
        }
