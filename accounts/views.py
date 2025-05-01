from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.models import User
from django.db.models import Q
from pathlib import Path


from .forms import AlunoForm
from .models import Aluno
from moderator.models import Material, Pedido
from moderator.forms import PedidoForm
from emprestimos.models import Emprestimo
# Create your views here.

def RegisterPage(request):
    form = UserCreationForm()
    alunoForm = AlunoForm()

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        alunoForm = AlunoForm(request.POST)
        
        if form.is_valid() and alunoForm.is_valid():

            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            
            aluno = alunoForm.save(commit=False)
            aluno.user = user
            aluno.save()


            login(request, user)
            return redirect('dashboard-aluno')
        else:
            messages.error(request, 'Ocorreu um erro durante o registro!')


    context = {
        'form':form,
        'alunoForm': alunoForm,
    }
    return render(request, 'accounts/cadastrar.html', context)


def LoginPage(request):

    if request.user.is_authenticated:
        return redirect('dashboard-aluno')

    if request.method == 'POST':
        matricula = request.POST.get('matricula')
        password = request.POST.get('password')

        try:
            username = Aluno.objects.get(matricula=matricula).user.username
        except:
            messages.error(request, 'Usuário não existe!')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('dashboard-aluno')
        else:
            messages.error(request, 'Nome de usuário OU senha estão erradas!')

    context = {

    }
    return render(request, "accounts/login.html", context)


@login_required(login_url='/login/')
def LogoutUser(request):
    logout(request)
    return redirect('dashboard-aluno')


@login_required(login_url='/login/')
def DashboardAluno(request):
    context = {
            'pedidos_pendentes':Pedido.objects.filter(
                aluno=Aluno.objects.get(user=request.user), 
                pendência=True
                ),
            'pedidos_respondidos':Pedido.objects.filter(
                aluno=Aluno.objects.get(user=request.user), 
                pendência=False,
                ),
            'emprestimos':Emprestimo.objects.filter(
                aluno=Aluno.objects.get(user=request.user), 
                ),
       }
    return render(request, "accounts/dashboard.html", context)