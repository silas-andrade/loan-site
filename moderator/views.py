from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from datetime import datetime
from django.http import HttpResponse, JsonResponse
from .models import Material, LoanApplication
from loans.models import Loan
from accounts.models import User


@login_required(login_url='/login/')
def DashboardAdmin(request):
    """
    Mostra aos moderadores todos os pedidos pendentes 
    e materias disponíveis  
    """
    if not request.user.is_staff:
        return redirect('dashboard')
    
    else:
        context = {
            'pedidos':LoanApplication.objects.filter(is_pending=True),
            'materiais':Material.objects.filter(available_quantity__gte=1),
            'emprestimos_esperando_devolucao':Loan.objects.filter(is_returned=False),
            'emprestimos_esperando_confimacao_de_devolucao':Loan.objects.filter(is_returned=True, is_return_confirmed=False),
        }
        return render(request, "moderator/dashboard.html", context)


@login_required(login_url='/login/')
def ManageUsers(request):
    ...
    """
    if not request.user.is_staff:
        return redirect('dashboard')
    
    else:
        context = {
            'alunos':User.objects.filter(moderador=False),
            'admins':User.objects.filter(moderador=True)
        }
        

        return render(request, "moderator/lista_usuario.html", context)
    """ 
    return redirect('dashboard') if not request.user.is_staff else redirect('dashboard-admin')


@login_required(login_url='/login/')
def ViewAllLoans(request):
    user = User.objects.get(username=request.user)
    emprestimos_devolvidos = list(
         Loan.objects.filter(user=user, is_return_confirmed=True)
    )
    emprestimos_nao_devolvidos = list(
         Loan.objects.filter(user=user, is_return_confirmed=False)
    )
    
    context = {
        'emprestimos_devolvidos':emprestimos_devolvidos,
        'emprestimos_nao_devolvidos':emprestimos_nao_devolvidos,
    }
    return render(request, "moderator/ver_emprestimos.html", context)


@login_required(login_url='/login/')
def BlockUser(request, pk):
    if not request.user.is_staff:
        return redirect('dashboard')
    
    else:
        user = User.objects.get(id=pk)

        if user.is_blocked:
            user.is_blocked = False
        else:
            user.is_blocked = True

        user.save()
    return redirect('dashboard-admin')

@login_required(login_url='/login/')
def ViewMaterials(request):
    if request.user.is_staff:
        materias = Material.objects.all()
        context = {
            'materiais':materias,   
        }
        return render(request, "moderator/material.html", context)
    else:
        return JsonResponse("<h1>Você não pode entrar aqui!</h1>")
    

@login_required(login_url='/login/')
def DeleteMaterial(request, pk):
    if request.user.is_staff:
        materiais = Material.objects.get(id=pk)
        materiais.delete()
        return redirect('dashbdashboard-adminoard')
    else:
        return JsonResponse("<h1>Você não pode entrar aqui!</h1>")


@login_required(login_url='/login/')
def AcceptMaterialReturn(request, pk):
    if not request.user.is_staff:
        return redirect('dashboard')
    else:
        loan = Loan.objects.get(id=pk)
        if loan.is_returned:
            loan.return_confirmed = True
            loan.date_returned = datetime.now()
            loan.save()

            material = Material.objects.get(nome=loan.material)
            material.available_quantity += loan.quantity
            material.save()

            return redirect('dashboard-admin')
        return redirect('dashboard-admin')


@login_required(login_url='/login/')
def AcceptLoanApplication(request, pk):
    if not request.user.is_staff:
        return redirect('dashboard')
    else:
        loan_application = LoanApplication.objects.get(id=pk)
        material = Material.objects.get(name=loan_application.material.name)
        if loan_application.is_pending and material.available_quantity >= loan_application.quantity and loan_application.quantity > 0:
            loan_application.is_pending = False
            loan_application.is_approved = True
            loan_application.save()

            material.available_quantity -= loan_application.quantity
            material.save()
            
            Loan.objects.create(
                user=loan_application.user,
                material=material,
                expected_return_date=loan_application.expected_return_date,
                quantity=loan_application.quantity,
                who_approved=User.objects.get(username=request.user)
            )
            return redirect('dashboard-admin')
        return redirect('dashboard-admin')
        


@login_required(login_url='/login/')
def RejectLoanApplication(request, pk):
    if not request.user.is_staff:
        return redirect('dashboard')
    else:
        loan_application = LoanApplication.objects.get(id=pk)
        if loan_application.is_pending:
            loan_application.is_pending = False
            loan_application.is_approved = False
            loan_application.save()
            return redirect('dashboard-admin')
        return redirect('dashboard-admin', {"warning":"This request has already been fulfilled"})