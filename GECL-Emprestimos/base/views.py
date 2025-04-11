from django.shortcuts import render, get_object_or_404, redirect

def dashboard(request):
    return render(request, "base/dashboard.html")

def LoginPage(request):
    pass