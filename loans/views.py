from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from moderator.forms import LoanApplicationForm
from .models import Loan
from accounts.models import User


@login_required(login_url='/sing-in/')
def RequestLoan(request):
    form = LoanApplicationForm()

    if request.method == 'POST':
        user = User.objects.get(username=request.user)
        form = LoanApplicationForm(request.POST)
        if form.is_valid:
            if not user.is_blocked:
                pedido = form.save(commit=False)
                pedido.user = user
                pedido.save()
                return redirect('dashboard')
            else:
                return HttpResponse('<h1>Você está proibido de fazer empréstimos</h1>')
        
    context = {
        'form':form,   
    }
    return render(request, "loans/solicitar_emprestimos.html", context)


@login_required(login_url='/sing-in/')
def MakeLoanReturn(request, pk):
    loan = Loan.objects.get(id=pk)

    if loan.user.username == request.user:
        loan.returned = True
        loan.save()
        return redirect('dashboard')
    else:
        return HttpResponse('<h1>Você não pode fazer isso!</h1>')