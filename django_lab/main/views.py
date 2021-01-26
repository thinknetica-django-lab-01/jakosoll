from django.shortcuts import render


def index(request):
    """Displays main page"""
    turn_on_block: bool = False
    return render(request, 'index.html', {'turn_on_block': turn_on_block})
