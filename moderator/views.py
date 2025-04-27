from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from datetime import datetime
from django.http import HttpResponse, JsonResponse
from .models import Material, Pedido
from emprestimos.models import Emprestimo
from accounts.models import Aluno


@login_required(login_url='/login/')
def DashboardAdmin(request):
    """
    Mostra aos moderadores todos os pedidos pendentes 
    e materias disponíveis  
    """
    if request.user.is_staff == False:
        return redirect('dashboard-aluno')
    
    else:
        context = {
            'pedidos':Pedido.objects.filter(pendência=True),
            'materiais':Material.objects.filter(quantidade_disponivel__gte=1),
            'emprestimos_esperando_devolucao':Emprestimo.objects.filter(devolvido=False),
            'emprestimos_esperando_confimacao_de_devolucao':Emprestimo.objects.filter(devolvido=True, devolução_confirmada=False),
        }
        return render(request, "moderator/dashboard.html", context)


@login_required(login_url='/login/')
def GerenciarAlunos(request):
    if request.user.is_staff == False:
        return redirect('dashboard-aluno')
    
    else:
        context = {
            'alunos':Aluno.objects.filter(moderador=False),
            'admins':Aluno.objects.filter(moderador=True)
        }
        

        return render(request, "moderator/lista_usuario.html", context)


@login_required(login_url='/login/')
def VerTodosOsEmprestimos(request):
    aluno = Aluno.objects.get(user=request.user)
    emprestimos = list(
         Emprestimo.objects.filter(aluno=Aluno.objects.get(user=request.user))
         )
    pedidos = list(
         Pedido.objects.filter(aluno=aluno)
         )
    context = {
        'emprestimos':emprestimos,
        'pedidos':pedidos
    }
    return render(request, "moderator/ver_emprestimos.html", context)




@login_required(login_url='/login/')
def BloquearUsuarios(request, pk):
    if request.user.is_staff == False:
        return redirect('dashboard-aluno')
    
    else:
        aluno = Aluno.objects.get(id=pk)

        if aluno.bloqueado:
            aluno.bloqueado = False
        else:
            aluno.bloqueado = True

        aluno.save()
    return JsonResponse({
            'aluno':aluno.nome_completo,
            'bloqueado':aluno.bloqueado
        })

@login_required(login_url='/login/')
def VerMateriais(request):
    if request.user.is_staff:
        materias = Material.objects.all()
        context = {
            'materiais':materias,   
        }
        return render(request, "moderator/material.html", context)
    else:
        return HttpResponse("<h1>Você não pode entrar aqui!</h1>")
    

@login_required(login_url='/login/')
def RemoverMateriais(request, pk):
    if request.user.is_staff:
        materiais = Material.objects.delete(id=pk)
        return redirect('dashboard')
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
            emprestimo.save()

            material = Material.objects.get(nome=emprestimo.material)
            material.quantidade_disponivel += emprestimo.quantidade
            material.save()

            return redirect('dashboard')
        return redirect('dashboard')


@login_required(login_url='/login/')
def AceitarPedido(request, pk):
    if request.user.is_staff == False:
        return redirect('dashboard-aluno')
    else:
        pedido = Pedido.objects.get(id=pk)
        material = Material.objects.get(nome=pedido.material.nome)
        if pedido.pendência == True and material.quantidade_disponivel >= pedido.quantidade:
            pedido.pendência = False
            pedido.aprovado = True
            pedido.save()

            material.quantidade_disponivel -= pedido.quantidade
            material.save()
            
            Emprestimo.objects.create(
                aluno=pedido.aluno,
                material=material,
                data_prevista=pedido.data_prevista,
                quantidade=pedido.quantidade
            )
            return redirect('dashboard')
        return HttpResponse('<h1>Ou o pedido já foi respondido ou o quantidade de material<br>pedido é maior do que a quantidade disponível</h1>')
        


@login_required(login_url='/login/')
def RecusarPedido(request, pk):
    if request.user.is_staff == False:
        return redirect('home')
    else:
        pedido = Pedido.objects.get(id=pk)
        if pedido.pendência == True:
            pedido.pendência = False
            pedido.aprovado = False
            pedido.save()
            return redirect('dashboard')
        return redirect('dashboard')