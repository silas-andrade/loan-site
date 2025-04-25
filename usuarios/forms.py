from django.forms import ModelForm
from .models import Aluno
from django import forms


class AlunoForm(ModelForm):
    class Meta:
        model = Aluno
        fields = '__all__'
        exclude = ['user', 'bloqueado', 'moderador']
        widgets = {
            'matricula':forms.TextInput(attrs={'class': 'form-control'}),
            'curso':forms.TextInput(attrs={'class': 'form-control'}),
        }