from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^new/$', 'EternalDraft.views.submit_page'),
    url(r'^decks/$', 'EternalDraft.views.decks'),
    url(r'^card_stats/$', 'EternalDraft.views.card_stats'),
)
