from django.contrib import admin
from django.urls import path

from usuarios.views import RegisterPage, LoginPage, LogoutUser, DashboardAluno
from emprestimos.views import SolicitarEmprestimo, FazerDevolucao

from moderator.views import (
    AceitarDevolucao, 
    AceitarPedido, 
    BloquearUsuarios, 
    DashboardAdmin, 
    GerenciarAlunos, 
    RecusarPedido, 
    RemoverMateriais, 
    VerMateriais, 
    VerTodosOsEmprestimos
    )

urlpatterns = [
    path('admin/', admin.site.urls), 
    
    # App Core

    # App usuarios
    path('registrar/', RegisterPage, name='cadastrar'),
    path('login/', LoginPage, name='login'),
    path('logout/', LogoutUser, name='logout'),

    # App Empréstimos
    path('solicitar/', SolicitarEmprestimo, name='solicitar'),
    #path('meus-emprestimos/', VerMeusEmprestimosPedidos, name='meus-emprestimos'),
    path('devolver/<str:pk>', FazerDevolucao, name='devolver'),

    # App Moderator
    path('dashboard/', DashboardAdmin, name='dashboard'),
    path('', DashboardAluno, name='dashboard-aluno'),

    path('ver-materiais/', VerMateriais, name='ver-materiais'),
    path('remover-materiais/<str:pk>', RemoverMateriais, name='remover-material'),
    
    path('aceitar-devolucao/<str:pk>', AceitarDevolucao, name='aceitar-devolucao'),
    
    path('aceitar-pedido/<str:pk>', AceitarPedido, name='aceitar-pedido'),
    path('recusar-pedido/<str:pk>', RecusarPedido, name='recusar-pedido'),
    
    
    path('todos-emprestimos/', VerTodosOsEmprestimos, name='todos-emprestimos'),




    path('gerenciar-alunos/', GerenciarAlunos, name='gerenciar-alunos'),
    path('bloquear-usuarios/<str:pk>', BloquearUsuarios, name='bloquear-usuarios'),


]
