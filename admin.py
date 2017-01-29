from django.contrib import admin
from EternalDraft.models import Deck, Card

class DeckAdmin(admin.ModelAdmin):
    list_display = ('wins', 'losses', 'colors', 'create_date')

class CardAdmin(admin.ModelAdmin):
    list_display = ('name', 'colors')
    search_fields = ['name']

admin.site.register(Card, CardAdmin)
admin.site.register(Deck, DeckAdmin)