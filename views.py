from django import forms
from django.shortcuts import render_to_response
from django.shortcuts import render
from django.http import HttpResponseRedirect
from EternalDraft.models import *
from django.utils import timezone
from django.views.generic.edit import DeleteView
from django.core.urlresolvers import reverse_lazy
from django.db.models import Sum
from django.contrib.auth.decorators import login_required

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

@login_required(login_url='/eternal/login/')
def decks(request):
    # todo: faded color icons
    decks = Deck.objects.all()
    return render(request, 'decks.html', {'decks': decks})
        
#  TODO: https://docs.djangoproject.com/en/1.10/topics/db/aggregation/
#   associate aggregates with the objects
# q = cards.annotate(Sum('deck__wins', distinct=True), Sum('deck__losses', distinct=True))
@login_required(login_url='/eternal/login/')
def card_stats(request):
    # todo: scrape decklist card images
    cards = Card.objects.all()
    card_info = []
    for card in cards:
        decks = Deck.objects.filter(cards__id=card.id)
        num_decks = decks.count()
        aggregates = decks.aggregate(wins=Sum('wins'), losses=Sum('losses'))
        wins, losses = aggregates['wins'], aggregates['losses']
        if not wins and not losses: continue  # this happens if a card object is not in any decks
        card_info.append({
            'name': card.name,
            'cost': card.cost,
            'colors': card.colors,
            'decks': num_decks,
            'games': wins + losses,
            'winrate': str((100 * wins) / (wins + losses)) + "%",
        })
    card_info.sort(reverse=True, key=lambda x:x['winrate'])
    return render(request, 'card_stats.html', {'cards': card_info})

class DeleteDeck(DeleteView):
    model = Deck
    success_url = reverse_lazy('decks')
    template_name = 'delete_deck.html'