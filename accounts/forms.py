from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from accounts.models import User
from django import forms

class UserFormRegister(UserCreationForm):
    class Meta:
        model = User
        fields = ('full_name', 'username', 'course', 'email', 'password1', 'password2')
        labels = {
            'full_name':'Nome completo',
            'username':'Matrícula',
            'course': 'Curso',
            'email':'Email'
        }
        widgets = {
            'full_name':forms.TextInput(attrs={'class': 'form-control'}),
            'username':forms.TextInput(attrs={'class': 'form-control'}),
            'course':forms.Select(
                attrs={
                    'placeholder': 'Escolha o seu curso',
                    'class': 'form-control'
                    },
                choices=[
                        ('Informática', 'Informática'),
                        ('Agropecuária', 'Agropecuária'),
                        ('Alimentos', 'Alimentos'),
                        ('Zootecnia', 'Zootecnia'),
                    ]
                    ),
            'email':forms.EmailInput(attrs={'class': 'form-control'}),
        }