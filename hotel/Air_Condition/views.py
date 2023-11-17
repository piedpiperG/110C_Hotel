from django.shortcuts import render

# Create your views here.
from django.shortcuts import render


def websocket_view(request):
    return render(request, 'websocket.html')
