from django.contrib import admin
from django.urls import path, include

from usuarios.views import RegisterPage, LoginPage
from core.views import HomePage
from emprestimos.views import SolicitarEmprestimo, VerMeusEmprestimosPedidos, FazerDevolucao
from moderator.views import DashboardAdmin, VerAlterarMateriais

urlpatterns = [
    path('admin/', admin.site.urls), 
    
    # App Core
    path('', HomePage, name='home'),

    # App usuarios
    path('registrar/', RegisterPage, name='registrar'),
    path('login/', LoginPage, name='login'),

    # App Empréstimos
    path('solicitar/', SolicitarEmprestimo, name='solicitar'),
    path('meus-emprestimos/', VerMeusEmprestimosPedidos, name='meus-emprestimos'),
    path('devolver/', FazerDevolucao, name='devolver'),

    # App Moderator
    path('dashboard/', DashboardAdmin, name='dashboard'),
    path('ver-materiais/', VerAlterarMateriais, name='ver-materiais'),

]
