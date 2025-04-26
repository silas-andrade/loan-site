from django.db import models
from usuarios.models import Aluno
# Create your models here.
class Material(models.Model):
    nome = models.CharField(max_length=50)
    quantidade_total = models.PositiveIntegerField(default=0)
    quantidade_disponivel = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.nome
    
class Pedido(models.Model):
    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE)
    material = models.ForeignKey(Material, on_delete=models.CASCADE)
    criado = models.DateTimeField(auto_now_add=True)
    data_prevista = models.DateTimeField()
    pendência = models.BooleanField(default=True) 
    aprovado = models.BooleanField(default=False)