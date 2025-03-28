from django.shortcuts import render

def home (request):
    return render(request, 'proposta/home.html')

