from django.shortcuts import render
from qanda.models import Question
from courses.models import OurCourse
from accounts.models import Account


def HomePageView(request):
	context = {}
	land_context = {}
	all_questions = Question.objects.all()
	our_courses = OurCourse.objects.all().order_by('date_created')[:6]
	land_context['our_courses'] = our_courses
	our_teachers = Account.objects.filter(is_our_teacher=1)
	context['questions'] = all_questions
	if request.user.is_authenticated:
		user_image = request.user.profile_pic.image.url
		context['user_image'] = user_image
		return render(request, 'homepage/homepage.html', context)
	else:
		return render(request, 'homepage/landing_page.html', land_context)