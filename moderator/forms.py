from django.forms import ModelForm
from .models import LoanApplication
from django import forms


class LoanApplicationForm(ModelForm):
    class Meta:
        model = LoanApplication
        fields = ['material', 'quantity', 'expected_return_date']
        widgets = {
            'material': forms.Select(attrs={'placeholder': 'Escolha o material'}),
            'quantity': forms.NumberInput(attrs={'placeholder': 'Escolha a quantidade de material'}),
            'expected_return_date': forms.DateTimeInput(
                attrs={
                    'type': 'datetime-local',
                    'placeholder': 'Escolha a data e hora'
                }
            ),
        }
        labels = {
            'material': 'Material',
            'expected_return_date': 'Data prevista para devolução'
        }
    