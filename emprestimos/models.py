from django.db import models
from usuarios.models import *
from moderator.models import *
# Create your models here.

class Emprestimo(models.Model):
    aluno = models.ForeignKey(Aluno, on_delete=models.DO_NOTHING)
    material = models.ForeignKey(Material, on_delete=models.DO_NOTHING)
    quantidade = models.PositiveIntegerField()
    data_prevista = models.DateTimeField()
    created = models.DateTimeField(auto_now_add=True)
    data_devolvida = models.DateTimeField(blank=True, null=True)
    devolvido = models.BooleanField(default=False)
    devolução_confirmada = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.aluno} | {self.material} | {self.devolvido} | {self.devolução_confirmada}'