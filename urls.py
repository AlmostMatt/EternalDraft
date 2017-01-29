from django.conf.urls import patterns, url
from views import DeleteDeck

urlpatterns = patterns('',
    url(r'^new/$', 'EternalDraft.views.submit_page', name='new'),
    url(r'^decks/$', 'EternalDraft.views.decks', name='decks'),
    url(r'^card_stats/$', 'EternalDraft.views.card_stats', name='card_stats'),
    url(r'^delete_deck/(?P<pk>\w+)/$', DeleteDeck.as_view(), name="delete_deck"),
)
