from django.contrib import admin
from django.urls import path

from accounts.views import RegisterPage, LoginPage, LogoutUser, DashboardUser
from loans.views import RequestLoan, MakeLoanReturn

from moderator.views import (
    AcceptMaterialReturn, 
    AcceptLoanApplication,
    BlockUser, 
    DashboardAdmin, 
    ManageUsers, 
    RejectLoanApplication, 
    DeleteMaterial, 
    ViewMaterials, 
    ViewAllLoans
    )


urlpatterns = [
    path('admin/', admin.site.urls), 
    
    # App Core

    # App usuarios
    path('sing-up/', RegisterPage, name='sing-up'),
    path('sing-in/', LoginPage, name='sing-in'),
    path('logout/', LogoutUser, name='logout'),

    # App Empréstimos
    path('request-loan/', RequestLoan, name='request-loan'),
    #path('meus-loans/', VerMeusEmprestimosPedidos, name='meus-emprestimos'),
    path('return-loan/<str:pk>', MakeLoanReturn, name='return-loan'),

    # App Moderator
    path('dashboard-admin/', DashboardAdmin, name='dashboard-admin'),
    path('', DashboardUser, name='dashboard'),

    path('view-materials/', ViewMaterials, name='view-materials'),
    path('delete-material/<str:pk>', DeleteMaterial, name='delete-material'),
    
    path('accept-material-return/<str:pk>', AcceptMaterialReturn, name='accept-material-return'),
    
    path('accept-loan-application/<str:pk>', AcceptLoanApplication, name='accept-loan-application'),

    path('reject-loan-application/<str:pk>', RejectLoanApplication, name='reject-loan-application'),
    
    
    path('all-loans/', ViewAllLoans, name='all-loans'),

    path('manage-users/', ManageUsers, name='manage-users'),

    path('block-user/<str:pk>', BlockUser, name='block-user'),


]
