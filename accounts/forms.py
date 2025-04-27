from django.forms import ModelForm
from accounts.models import Aluno
from django import forms


class AlunoForm(ModelForm):
    class Meta:
        model = Aluno
        fields = '__all__'
        exclude = ['user', 'bloqueado', 'moderador']
        widgets = {
            'nome_completo':forms.TextInput(attrs={'class': 'form-control'}),
            'matricula':forms.TextInput(attrs={'class': 'form-control'}),
            'curso':forms.TextInput(attrs={'class': 'form-control'}),
        }