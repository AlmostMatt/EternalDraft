from django import forms
from django.shortcuts import render_to_response
from django.shortcuts import render
from django.http import HttpResponseRedirect

def submit_page(request):
    if request.method == 'POST':
        # do some work
        return HttpResponseRedirect('/eternal/new/')
    else:
        form = SubmitForm()
        return render(request, 'submit_page.html',
            {'form': form})

class SubmitForm(forms.Form):
    cards = forms.CharField(label='Cards', initial="Paste decklist here")
    wins = forms.IntegerField(label='Wins', initial=3)
    losses = forms.IntegerField(label='Losses', initial=3)
