from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models
from django.db import models
from django.utils import timezone
from django.conf import settings


class UsuarioManager(BaseUserManager):
    def create_user(self, matricula, nome, turma, ano, password=None, email=None, cargo=None):
        if not matricula:
            raise ValueError("O usuário deve ter uma matrícula válida.")
        user = self.model(
            matricula=matricula,
            nome=nome,
            turma=turma,
            ano=ano,
            email=email,
            cargo=cargo
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, matricula, nome, turma, ano, password=None, email=None, cargo=None):
        user = self.create_user(
            matricula,
            nome,
            turma,
            ano,
            password=password,
            email=email,
            cargo=cargo
        )
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class Usuario(AbstractBaseUser):
    matricula = models.CharField(max_length=20, unique=True)
    nome = models.CharField(max_length=255)
    turma = models.CharField(max_length=10)
    ano = models.CharField(max_length=10)
    email = models.EmailField(max_length=255, blank=True, null=True)
    cargo = models.CharField(max_length=255, blank=True, null=True)
    bloqueado = models.BooleanField(default=False)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'matricula'
    REQUIRED_FIELDS = ['nome', 'turma', 'ano']

    objects = UsuarioManager()

    def __str__(self):
        return self.nome

    def clean(self):
     
        super().clean()

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True


# Material

class Material(models.Model):
    nome = models.CharField(max_length=20)
    quantidade_total = models.PositiveIntegerField()
    quantidade_disponivel = models.PositiveIntegerField()

    def __str__(self):
        return self.nome


class EmprestimoMaterial(models.Model):
    PENDENTE = 'P'
    ACEITO = 'A'
    DEVOLVIDO = 'D'
    
    STATUS_CHOICES = [
        (PENDENTE, 'Pendente'),
        (ACEITO, 'Aceito'),
        (DEVOLVIDO, 'Devolvido'),
    ]
    
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  #
    material = models.ForeignKey(Material, on_delete=models.CASCADE)
    quantidade = models.PositiveIntegerField()
    data_emprestimo = models.DateField(default=timezone.now)
    data_prevista_devolucao = models.DateField()
    data_devolucao = models.DateField(blank=True, null=True)
    devolvido = models.BooleanField(default=False)
    status = models.CharField(
        max_length=1,
        choices=STATUS_CHOICES,
        default=PENDENTE,  #
    )

    def __str__(self):
        return f"{self.usuario.username} pegou {self.quantidade}x {self.material.nome}"

    def atrasado(self):
        return not self.devolvido and timezone.now().date() > self.data_prevista_devolucao




# Configurações de empréstimo

class Configuracao(models.Model):
    aceitar_automaticamente = models.BooleanField(default=False)
    bloquear_emprestimos = models.BooleanField(default=False)

    def __str__(self):
        return "Configurações do Sistema"


