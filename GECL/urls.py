from django.contrib import admin
from django.urls import path

from usuarios.views import RegisterPage, LoginPage
from core.views import HomePage
from emprestimos.views import SolicitarEmprestimo, VerMeusEmprestimosPedidos, FazerDevolucao
from moderator.views import DashboardAdmin, VerAlterarMateriais, AceitarDevolucao, AceitarPedido, RecusarPedido

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
    path('aceitar-devolucao/<int:pk>', AceitarDevolucao, name='aceitar-devolucao'),
    path('aceitar-pedido/<int:pk>', AceitarPedido, name='aceitar-pedido'),
    path('recusar-pedido/<int:pk>', RecusarPedido, name='recusar-pedido'),


]
