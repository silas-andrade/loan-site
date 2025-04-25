from django.shortcuts import render

# Create your views here.

def HomePage(request):

    context = {
        
    }

    return render(request, "core/home.html", context)