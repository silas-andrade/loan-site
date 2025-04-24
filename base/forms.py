from django import forms
from .models import Material,EmprestimoMaterial,Usuario

class MaterialForm(forms.ModelForm):
    class Meta:
        model = Material
        fields = ['nome', 'quantidade_total']
        widgets = {
            'nome': forms.TextInput(attrs={
                'placeholder': 'Nome do material',
                'class': 'flex-1 border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-400 min-w-[200px]'
            }),
            'quantidade_total': forms.NumberInput(attrs={
                'placeholder': 'Quantidade',
                'class': 'w-32 border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-400'
            }),
        }




class UsuarioCadastroForm(forms.ModelForm):
    ANOS = [('1º Ano', '1º Ano'), ('2º Ano', '2º Ano'), ('3º Ano', '3º Ano')]
    TURMAS = [(letra, f'Turma {letra}') for letra in 'ABCDEFGH']

    ano = forms.ChoiceField(choices=ANOS)
    turma = forms.ChoiceField(choices=TURMAS)
    senha = forms.CharField(widget=forms.PasswordInput())
    confirmar_senha = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = Usuario
        fields = ['nome', 'matricula', 'ano', 'turma', 'senha']

    def clean(self):
        cleaned_data = super().clean()
        senha = cleaned_data.get("senha")
        confirmar = cleaned_data.get("confirmar_senha")

        if senha and confirmar and senha != confirmar:
            self.add_error('confirmar_senha', "As senhas não coincidem.")



class EmprestimoForm(forms.ModelForm):
    class Meta:
        model = EmprestimoMaterial
        fields = ['material', 'quantidade', 'data_prevista_devolucao']
        widgets = {
            'data_prevista_devolucao': forms.DateInput(attrs={'type': 'date'}),
        }
        labels = {
            'material': 'Material',
            'quantidade': 'Quantidade desejada',
            'data_prevista_devolucao': 'Data prevista para devolução',
        }

    def clean_quantidade(self):
        quantidade = self.cleaned_data.get('quantidade')
        material = self.cleaned_data.get('material')

        if quantidade and material:
            if quantidade > material.quantidade_disponivel:
                raise forms.ValidationError(f"Apenas {material.quantidade_disponivel} disponíveis.")
        return quantidade
