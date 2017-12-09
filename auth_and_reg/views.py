from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect

from auth_and_reg.forms import SignUpForm


def sign_up(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('core:index')
    else:
        form = SignUpForm()
    return render(request, 'auth_and_reg/sign_up.html', {'form': form})
