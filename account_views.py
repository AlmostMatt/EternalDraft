from django.utils.http import is_safe_url
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login

def register(request):
    if request.method =='POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            new_user = authenticate(username=form.cleaned_data['username'],
                                    password=form.cleaned_data['password1'],)
            login(request, new_user)
            redirect_to = request.POST.get('next', '')
            if is_safe_url(url=redirect_to, host=request.get_host()):
                return HttpResponseRedirect(redirect_to)
            else:
                return HttpResponseRedirect('/eternal/')
    else:
        form = UserCreationForm() # A new form
    return render_to_response('registration/register.html', {
        'form': form,
        'next': request.GET.get('next', '')
    }, context_instance=RequestContext(request))