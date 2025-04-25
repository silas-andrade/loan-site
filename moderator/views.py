from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from datetime import datetime
from django.http import HttpResponse
from .models import Material, Pedido
from emprestimos.models import Emprestimo


@login_required(login_url='/login/')
def DashboardAdmin(request):
    """
    Mostra aos moderadores todos os pedidos pendentes 
    e materias disponíveis  
    """
    if request.user.is_staff == False:
        return redirect('home')
    else:
        context = {
            'pedidos':Pedido.objects.filter(aprovado=False),
            'materiais':Material.objects.filter(quantidade_disponivel__gte=1),
        }
        return render(request, "moderator/dashboard.html", context)


@login_required(login_url='/login/')
def VerAlterarMateriais(request):
    if request.user.is_staff:
        materias = Material.objects.all()
        context = {
            'materiais':materias,   
        }
        return render(request, "moderator/material.html", context)
    else:
        return HttpResponse("<h1>Você não pode entrar aqui!</h1>")
    

@login_required(login_url='/login/')
def AceitarDevolucao(request, pk):
    if request.user.is_staff == False:
        return redirect('home')
    else:
        emprestimo = Emprestimo.objects.get(id=pk)
        if emprestimo.devolvido == True:
            emprestimo.devolução_confirmada = True
            emprestimo.data_devolvida = datetime.now()
            return redirect('dashboard')
        return redirect('dashboard')


@login_required(login_url='/login/')
def AceitarPedido(request, pk):
    if request.user.is_staff == False:
        return redirect('home')
    else:
        pedido = Pedido.objects.get(id=pk)
        if pedido.pendência == False:
            pedido.pendência = True
            pedido.aprovado = True
            Emprestimo.objects.create(
                aluno=pedido.aluno,
                material=pedido.material,
                data_prevista=pedido.data_prevista,
            )
            return redirect('home')
        return redirect('home')
        


@login_required(login_url='/login/')
def RecusarPedido(request, pk):
    if request.user.is_staff == False:
        return redirect('home')
    else:
        pedido = Pedido.objects.get(id=pk)
        if pedido.pendência == False:
            pedido.pendência = True
            pedido.aprovado = False
            return redirect('home')
        return redirect('home')