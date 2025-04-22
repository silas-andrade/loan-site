from django.urls import path
from . import views

urlpatterns = [
    path('', views.loginPage, name='login'),
    path('cadastrar/', views.cadastrar, name='cadastrar'),
    
    path('indexAdm/', views.indexAdm, name='indexAdm'),
    path('aceitar/<int:pedido_id>/', views.aceitar_pedido, name='aceitar_pedido'),
    path('recusar/<int:pedido_id>/', views.recusar_pedido, name='recusar_pedido'),
    path('confirmar_devolucao/<int:pedido_id>/', views.confirmar_devolucao, name='confirmar_devolucao'),
    path('recusar_devolucao/<int:pedido_id>/', views.recusar_devolucao, name='recusar_devolucao'),


    path('material/', views.materiais, name='material'),
    path('material/remover/<int:id>/', views.remover_material, name='remover_material'),

    path('lista_usuario/', views.usuarios_view , name='lista_usuario'),
    path('bloquear_usuario/<int:usuario_id>/', views.bloquear_usuario, name='bloquear_usuario'),

    path('configuracoes/', views.configuracoes, name='configuracoes'),

    path('emprestimo/', views.solicitar_emprestimo, name='emprestimo'),

]
