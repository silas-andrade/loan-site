from django.db import models
from usuarios.models import *
from moderator.models import *
# Create your models here.

class Emprestimo(models.Model):
    aluno = models.ForeignKey(Aluno, on_delete=models.DO_NOTHING)
    material = models.ForeignKey(Material, on_delete=models.DO_NOTHING)
    data_prevista = models.DateTimeField()
    created = models.DateTimeField(auto_now_add=True)
    data_devolvida = models.DateTimeField()
    devolvido = models.BooleanField(default=False)
    devolução_confirmada = models.BooleanField(default=False)