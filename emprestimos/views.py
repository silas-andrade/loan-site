from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from moderator.forms import PedidoForm
from moderator.models import Pedido
from .models import Emprestimo
from usuarios.models import Aluno


@login_required(login_url='login/')
def SolicitarEmprestimo(request):
    form = PedidoForm()

    if request.method == 'POST':
        form = PedidoForm(request.POST)
        if form.is_valid:
            form.save(commit=False)
            Pedido.objects.create(
                aluno=Aluno.objects.get(user=request.user),
                material=form.material,
                data_prevista=form.data_prevista,
            )
    context = {
        'form':form
    }
    return render(request, "emprestimos/solicitar_emprestimos.html", context)


@login_required(login_url='login/')
def VerMeusEmprestimosPedidos(request):
    emprestimos = list(
         Emprestimo.objects.filter(aluno=Aluno.objects.filter(user=request.user))
         )
    pedido = list(
         Pedido.objects.filter(aluno=Aluno.objects.filter(user=request.user))
         )
    context = {
        'emprestimos':emprestimos,
        'pedido':pedido
    }
    return render(request, "emprestimos/ver_emprestimos.html", context)


@login_required(login_url='login/')
def FazerDevolucao(request, pk):
    emprestimo = Emprestimo.objects.filter(id=pk)

    if emprestimo.aluno.user == request.user:
        emprestimo.devolvido = True
        return redirect('home')
    else:
        return HttpResponse('<h1>Você não pode fazer isso!</h1>')

