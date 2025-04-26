from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.db import models



class Aluno(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    nome_completo = models.CharField(max_length=255)

    matricula = models.CharField(max_length=15, unique=True)

    curso = models.CharField(blank=True, null=True, max_length=15)

    bloqueado = models.BooleanField(default=False)

    moderador = models.BooleanField(default=False)

    
    def __str__(self):
        return self.user.username
    
