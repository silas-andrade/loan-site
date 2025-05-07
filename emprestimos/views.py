from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from moderator.forms import PedidoForm
from .models import Emprestimo
from accounts.models import Aluno


@login_required(login_url='/login/')
def SolicitarEmprestimo(request):
    form = PedidoForm()

    if request.method == 'POST':
        aluno = Aluno.objects.get(user=request.user)
        form = PedidoForm(request.POST)
        if form.is_valid:
            if not aluno.bloqueado:
                pedido = form.save(commit=False)
                pedido.aluno = aluno
                pedido.save()
                return redirect('dashboard-aluno')
            else:
                return HttpResponse('<h1>Você está proibido de fazer empréstimos</h1>')
        
    context = {
        'form':form,   
    }
    return render(request, "emprestimos/solicitar_emprestimos.html", context)


@login_required(login_url='/login/')
def FazerDevolucao(request, pk):
    emprestimo = Emprestimo.objects.get(id=pk)

    if emprestimo.aluno.user == request.user:
        emprestimo.devolvido = True
        emprestimo.save()
        return redirect('dashboard-aluno')
    else:
        return HttpResponse('<h1>Você não pode fazer isso!</h1>')