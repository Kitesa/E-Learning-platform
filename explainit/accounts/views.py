from django.shortcuts import render, redirect
from .forms import AccountCreationForm
from django.contrib import messages
from django.contrib.auth import login, authenticate

def AccountCreationPageView(request, *args, **kwargs):
	"""A FUNCTION FOR USER REGISTRATION 
		AUTHENTICATED USER HAVE NO PERMISSION TO ACCESS REGISTRATION PAGE
		UNLESS LOGGED OUT!!!
	"""
	if request.user.is_authenticated:
		messages.info(request, f'Logout first')
		return redirect('homepage:homepage')
	else:
		if request.method == 'POST':
			form = AccountCreationForm(request.POST)
			if form.is_valid():
				form.save()
				username 		= form.cleaned_data.get('username')
				email 			= form.cleaned_data.get('email')
				raw_password 	= form.cleaned_data.get('password1')
				account 		= authenticate(email=email, password=raw_password)
				login(request, account)
				messages.info(request, f'Your account has been created! You are now able to log in')
				return redirect('homepage:homepage')            
		else:
			form = AccountCreationForm()
		return render(request, 'accounts/account_creation_page.html', {'form': form})

