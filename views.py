from django import forms
from django.shortcuts import render_to_response
from django.shortcuts import render
from django.http import HttpResponseRedirect
from EternalDraft.models import *
from django.utils import timezone

def submit_page(request):
    if request.method == 'POST':
        cards = request.POST.get("cards", "")
        wins = request.POST.get("wins", "")
        losses = request.POST.get("losses", "")
        
        deck = new_deck(cards, wins, losses)
        return HttpResponseRedirect('/eternal/new/')
    else:
        form = SubmitForm()
        return render(request, 'submit_page.html',
            {'form': form})

class SubmitForm(forms.Form):
    cards = forms.CharField(label='Cards', initial="1 Inspire (Set1 #129)")
    wins = forms.IntegerField(label='Wins', initial=3)
    losses = forms.IntegerField(label='Losses', initial=3)

def decks(request):
    # todo: faded color icons
    decks = Deck.objects.all()
    return render(request, 'decks.html', {'decks': decks})
            
def card_stats(request):
    # todo: scrape decklist card images
    cards = Card.objects.all
    return render(request, 'card_stats.html', {'cards': cards})