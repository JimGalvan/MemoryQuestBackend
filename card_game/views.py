from django.shortcuts import render
from .models import Card

def game_view(request):
    cards = Card.objects.all()
    return render(request, 'card_game/game.html', {'cards': cards})
