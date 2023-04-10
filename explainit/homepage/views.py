from django.shortcuts import render

def HomePageView(request):
	if request.user.is_authenticated:
		return render(request, 'homepage/homepage.html')
	else:
		return render(request, 'homepage/landing_page.html')