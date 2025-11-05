from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages


from moderator.models import LoanApplication
from .forms import UserFormRegister
from loans.models import Loan
from .models import User


def RegisterPage(request):
    form = UserFormRegister()

    if request.method == 'POST':
        form = UserFormRegister(request.POST)
        
        if form.is_valid:

            user = form.save(commit=False)
            user.username = user.username.upper()
            user.save()

            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Ocorreu um erro durante o registro!')


    context = {
        'form':form,
    }
    return render(request, 'accounts/sing-up.html', context)


def LoginPage(request):

    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        matricula = request.POST.get('matricula')
        password = request.POST.get('password')

        try:
            username = User.objects.get(username=matricula).username
        except Exception as e:
            messages.error(request, 'Usuário não existe!')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Nome de usuário OU senha estão erradas!')

    context = {

    }
    return render(request, "accounts/sing-in.html", context)


@login_required(login_url='/sing-in/')
def LogoutUser(request):
    logout(request)
    return redirect('dashboard')


@login_required(login_url='/sing-in/')
def DashboardUser(request):
    print(request.user)
    context = {
            'pedidos_pendentes':LoanApplication.objects.filter(
                user=User.objects.get(username=request.user), 
                is_pending=True
                ),
            'pedidos_respondidos':LoanApplication.objects.filter(
                user=User.objects.get(username=request.user), 
                is_pending=False,
                ),
            'loans':Loan.objects.filter(
                user=User.objects.get(username=request.user), 
                ),
       }
    return render(request, "accounts/dashboard.html", context)