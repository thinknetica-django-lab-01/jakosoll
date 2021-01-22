from django.shortcuts import render


def index(request):
    """Displays main page"""
    return render(request, 'index.html')
