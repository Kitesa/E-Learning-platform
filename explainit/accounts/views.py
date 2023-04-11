from django.shortcuts import render, redirect
from .forms import AccountCreationForm
from django.contrib import messages
from django.contrib.auth import login, authenticate
from .models import TermsOfService
from django.views.generic import (ListView,)
from django.contrib.auth.decorators import login_required

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


class TermsOfServiceListView(ListView):
	model 			= TermsOfService
	template_name 	= 'accounts/terms_of_service.html'

	def get_context_data(self, *args, **kwargs):
		context = super(TermsOfServiceListView, self).get_context_data(*args, **kwargs)
		context['title'] = "ExplainIT-terms of service"
		context['terms_of_services'] = TermsOfService.objects.all()
		return context

@login_required
def UserProfileHomeView(request):
	current_user = request.user

	template = 'accounts/user_profile_home.html'
	return render(request, template)

@login_required
def update_user_profile(request):
	if request.method == 'POST':
		user_account_form = UserUpdateForm(request.POST, instance=request.user)
		if user_account_form.is_valid():
			user_account_form.save()
			messages.success(request, f'Your name has been updated!')
			return redirect('accounts:user-profile-home-view')
	else:
		user_account_form = UserUpdateForm(instance=request.user)
	
	context = {
		'user_account_form': user_account_form
    	}
	return render(request, 'accounts/account_profile_update.html', context)
