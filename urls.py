from django.conf.urls import url, include
from views import DeleteDeck

urlpatterns = [
    # auth urls are things like:  login, logged_out, password_change, password_reset, reset_confirmation
    url(r'^', include('django.contrib.auth.urls')),
    url(r'^register/$', 'EternalDraft.account_views.register', name='register'),
    url(r'^$', 'EternalDraft.views.decks', name='home'),
    url(r'^new_deck/$', 'EternalDraft.views.submit_page', name='new_deck'),
    url(r'^decks/$', 'EternalDraft.views.decks', name='decks'),
    url(r'^card_stats/$', 'EternalDraft.views.card_stats', name='card_stats'),
    url(r'^delete_deck/(?P<pk>\w+)/$', DeleteDeck.as_view(), name="delete_deck"),
]
