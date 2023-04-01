from django.shortcuts import render
from django.http import HttpResponse

def store(request):
    return render(request, 'store.html')