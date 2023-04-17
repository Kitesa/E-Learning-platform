from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import OurCourse
from .forms import OurCourseCreationForm
from django.views.generic import (ListView,
									CreateView,
									DetailView,
									)
from django.contrib.auth.mixins import (LoginRequiredMixin,
										UserPassesTestMixin,
										)
from django.contrib.auth.decorators import login_required
class OurCourseHomeView(ListView):
	'''
	 A class based view to show lists of
	 all couses on courses homepage
	'''
	model 			= OurCourse
	template_name 	= 'courses/our_courses_home_view.html'

	def get_context_data(self, *args, **kwargs):
		'''
			A django built in func to handle what will be passed
			to the template as what
		'''
		context = super(OurCourseHomeView, self).get_context_data(*args, **kwargs)
		context['title'] = "ExplainIT-Courses"
		context['our_courses'] = OurCourse.objects.all()
		return context

class OurCourseCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
	'''
	 A class based view used to create a course
	'''
	model 			= OurCourse
	form_class		= OurCourseCreationForm
	template_name 	= 'courses/course_creation_page.html'

	def form_valid(self, form):
		'''
		 Take the authenticated user as course instructor
		 '''
		form.instance.course_instructor = self.request.user
		return super().form_valid(form)

	def get_context_data(self, *args, **kwargs):
		'''
			A django built in func to handle what will be passed
			to the template as what
		'''
		context = super(OurCourseCreateView, self).get_context_data(*args, **kwargs)
		context['title'] = f'{self.request.user.username}-Create-Course'
		return context

	def test_func(self):
		if self.request.user.is_our_teacher:
			return True
		return False

class CourseDetailView(DetailView):
	model 			= OurCourse
	context_object_name = 'course'
	template_name	= 'courses/our_course_detail_view.html'

	def get_context_data(self, *args, **kwargs):
		course 	= self.get_object()
		context = super(CourseDetailView, self).get_context_data(*args, **kwargs)
		context['title'] = course.course_title
		return context


@login_required
def enroll_courses(request, pk):
    if request.method == 'GET':
        user = request.user
        course = get_object_or_404(OurCourse, pk=pk)

        if course.students.filter(id=user.id).exists():
            #user has already enrolled the course
            #remove students frpm enrolled student list
            course.students.remove(user)
            message=messages.success(request,f'You stopped learning {course.course_title}')
        else:
            course.students.add(user)
            message =messages.success(request, f'You enrolled {course.course_title}')
            total_students = {'total_students':course.total_students}
            return redirect(request.META.get('HTTP_REFERER'))
    return redirect(request.META.get('HTTP_REFERER'))