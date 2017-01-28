from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^new/$', 'EternalDraft.views.submit_page'),
    url(r'^submit_deck/$', 'EternalDraft.views.submit_deck'),
)
