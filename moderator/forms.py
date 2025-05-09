from django.forms import ModelForm
from .models import Pedido
from django import forms


class PedidoForm(ModelForm):
    class Meta:
        model = Pedido
        fields = ['material', 'quantidade', 'data_prevista']
        widgets = {
            'material': forms.Select(attrs={'placeholder': 'Escolha o material'}),
            'Quantidade': forms.NumberInput(attrs={'placeholder': 'Escolha o material'}),
            'data_prevista': forms.DateTimeInput(
                attrs={
                    'type': 'datetime-local',
                    'placeholder': 'Escolha a data e hora'
                }
            ),
        }
        labels = {
            'material': 'Material',
            'data_prevista': 'Data prevista para devolução'
        }
    