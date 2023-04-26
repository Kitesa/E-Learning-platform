from django.shortcuts import (render, 
								redirect,
								get_object_or_404,
								)
from .forms import (AccountCreationForm, 
					UserUpdateForm,
					ProfilePicUploadForm,
					)
from django.contrib import messages
from django.contrib.auth import login, authenticate, get_user_model
from .models import TermsOfService
from django.views.generic import (ListView, 
									CreateView, 
									UpdateView,
									DetailView,
									)
from django.contrib.auth.decorators import login_required
from .models import ProfilePic
from django.contrib.auth.mixins import (LoginRequiredMixin,
										UserPassesTestMixin,
										)
from accounts.models import Account

#ACCOUNT-ACTIVATION
from .tokens import AccountActivationToken
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage



def AccountActivationView(request, uidb64, token):
	try:
		uid = int(force_str(urlsafe_base64_decode(uidb64)))
		user = Account.objects.get(pk=uid)
		print(user)
	except:
		user = None

	if user is not None and AccountActivationToken.check_token(user, token):
		user.is_active = True
		user.save()

		messages.success(request, "Thank you for your email confirmation. Now you can login your account.")
		return redirect('accounts:login-page')
	else:
		messages.error(request, "Activation link is invalid!")

	return redirect('homepage:homepage')

def sendEmail(request, user, to_email):
	mail_subject = "Activate your user account."
	message = render_to_string("accounts/account_activation_page.html", {
		'user': user.username,
		'domain': get_current_site(request).domain,
		'uid': urlsafe_base64_encode(force_bytes(user.pk)),
		'token': AccountActivationToken.make_token(user),
		"protocol": 'https' if request.is_secure() else 'http'
	})
	email = EmailMessage(mail_subject, message, to=[to_email])
	if email.send():
		messages.success(request, f'Check your email to activate your account.')
	else:
		messages.error(request, f'Problem sending email to {to_email}, check if you typed it correctly.')


def AccountCreationPageView(request, *args, **kwargs):
	"""A FUNCTION FOR USER REGISTRATION 
		AUTHENTICATED USER HAVE NO PERMISSION TO ACCESS REGISTRATION PAGE
		UNLESS LOGGED OUT!!!
	"""
	if request.user.is_authenticated:
		messages.info(request, f'Logout first!!')
		return redirect('homepage:homepage')
	else:
		if request.method == 'POST':
			form = AccountCreationForm(request.POST)
			if form.is_valid():
				user = form.save()
				email = form.cleaned_data.get('email')
				sendEmail(request, user, email)

				return redirect('homepage:homepage')            
		else:
			form = AccountCreationForm()
		return render(request, 'accounts/account_creation_page.html', {'form': form})


class TermsOfServiceListView(ListView):
	'''
	class based view to show list of terms of service of explainit
	@ListView: django builtin class based view
	'''
	model 			= TermsOfService
	template_name 	= 'accounts/terms_of_service.html'

	def get_context_data(self, *args, **kwargs):
		'''
		returns what to send to the template
		'''
		context = super(TermsOfServiceListView, self).get_context_data(*args, **kwargs)
		context['title'] = "ExplainIT-terms of service"
		context['terms_of_services'] = TermsOfService.objects.all()
		return context

@login_required
def UserProfileHomeView(request):
	context = {}

	if request.user.is_authenticated:
		user_image = request.user.profile_pic.image.url
		context['user_image'] = user_image
	'''
	A function to manage user profile homepage
	'''
	current_user = request.user
	template = 'accounts/user_profile_home.html'
	return render(request, template, context)

@login_required
def UpdateUserProfile(request):
	'''
	a function to update user name 
	'''
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

class ProfilePicUpdateView(LoginRequiredMixin,UserPassesTestMixin, UpdateView):
	'''
	class based view to update the pp
	'''

	model = ProfilePic
	form_class = ProfilePicUploadForm
	template_name = 'profile_pic/profile_picture_update_view.html'

	def get_context_data(self, *args, **kwargs):
		'''
		returns a context that needs to be sent to template
		'''
		context = super(ProfilePicUpdateView, self).get_context_data(*args, **kwargs)
		context['title'] = f'{self.request.user} - Update profile picture'
		return context

	def test_func(self):
		'''
		authorization function, tests if the current user is
		the author of the pp
		'''
		profile_pic = self.get_object()
		if self.request.user == profile_pic.user:
			'''if profile_pic.image.url:
				profile_pic.image.delete(save=True)
			'''
			return True
		return False


class AccountDetailView(DetailView):

	model = Account
	template_name = 'accounts/account_detail_view_page.html'


	def get_context_data(self, *args, **kwargs):
		'''
		returns what to send to the template
		'''
		other_user = get_object_or_404(Account, pk=self.kwargs.get('pk'))
		context = super(AccountDetailView, self).get_context_data(*args, **kwargs)
		context['title'] = "ExplainIT-About"
		context['other_user'] = other_user
		return context

@login_required
def followunfollow(request, pk):
    if request.method == 'GET':
        user = request.user
        account = get_object_or_404(Account, pk=pk)

        if account.followers.filter(id=user.id).exists():
            #user has already enrolled the course
            #remove followers frpm enrolled student list
            account.followers.remove(user)
            message=messages.success(request,f'You stopped following {account.full_name}')
        else:
            account.followers.add(user)
            message =messages.success(request, f'You started following {account.full_name}')
            followers = {'total_followers':account.followers}
            return redirect(request.META.get('HTTP_REFERER'))
    return redirect(request.META.get('HTTP_REFERER'))

