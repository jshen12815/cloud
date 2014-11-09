# Social actions for clouddj
from django.shortcuts import render
from django.contrib.auth.decorators import login_required



def home(request):
    return render(request, 'index.html', {})

