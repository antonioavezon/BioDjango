from django.shortcuts import render

def resultado(request):
    return render(request, 'resultado/resultado.html')
