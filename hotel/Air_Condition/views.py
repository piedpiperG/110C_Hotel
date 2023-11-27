from django.shortcuts import render

# Create your views here.
from django.shortcuts import render


def monitor_init(request):
    return render(request, 'monitor.html')
