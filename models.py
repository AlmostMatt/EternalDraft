from django.db import models
from django.utils import timezone

class Deck(models.Model):
    cards = models.ManyToManyField(
        'Card',
        through='Contains',
        # through_fields = ('deck', 'card')  # only necessary for ambiguous relationships
    )
    wins = models.IntegerField(default=0)
    losses = models.IntegerField(default=0)
    create_date=models.DateTimeField('date created', db_index=True)
    colors = models.CharField(max_length=5)
    # TODO: add other aggregates like units, spells, power, influence (f t p j s)
    # also have a 'splash' field, and card count by color
    # and a "isSplash" attribute to the contains relationship (any color with <7 influence OR <7 cards)

class Card(models.Model):
    name = models.CharField(max_length=100)
    colors = models.CharField(max_length=2)
    # TODO:  manually add info like "evasive", "removal", "unit", "spell", "relic weapon", "curse", "power"
    # Probably dig through eternal files for some json data file or something

class Contains(models.Model):
    deck = models.ForeignKey(Deck, on_delete=models.CASCADE)
    card = models.ForeignKey(Card, on_delete=models.CASCADE)
    count = models.IntegerField(default=1)    

def new_deck(cards, w, l):
    card_objs = []
    for card_txt in cards.split(')'):
        card_txt = card_txt.strip()
        if not card_txt: continue  # for the last item
        count = int(card_txt.split(' ')[0])
        name = card_txt[card_txt.index(' ') + 1: card_txt.index(' (')]
        card, created = Card.objects.get_or_create(name=name, defaults={'colors': 'FTJPS'})
        card_objs.append((count, card))
    deck = Deck.objects.create(wins=w, losses=l, create_date=timezone.now(), colors='FTJPS')
    Contains.objects.bulk_create(
        [Contains(deck=deck, card=card_obj, count=count) for count, card_obj in card_objs])
    
# If cards is a raw string, cant search for decks by card
# If it is a many-to-many thing, I can query for decks that have a card but I think I lose the concept of count
# I can alternatively have a "many to one" relationship where every card corresponds to a deck, and I may have multiple instances of effectively identical card objects

# Having card objects is useful for card stats
# ManyToManyField.through allows additional data for the relationship (count!)