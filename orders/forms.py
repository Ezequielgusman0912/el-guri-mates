from django import forms

from .models import Order


class CheckoutForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['full_name', 'email', 'phone', 'address', 'notes']
        labels = {
            'full_name': 'Nombre completo',
            'email': 'Email',
            'phone': 'Teléfono / WhatsApp',
            'address': 'Dirección',
            'notes': 'Notas',
        }
        widgets = {
            'full_name': forms.TextInput(attrs={'placeholder': 'Nombre y apellido'}),
            'email': forms.EmailInput(attrs={'placeholder': 'tu@email.com'}),
            'phone': forms.TextInput(attrs={'placeholder': 'Ej: 351 123 4567'}),
            'address': forms.TextInput(attrs={'placeholder': 'Dirección de entrega (opcional)'}),
            'notes': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Alguna aclaración sobre tu pedido (opcional)'}),
        }
