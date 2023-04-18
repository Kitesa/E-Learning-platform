from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import OurCourse, CourseArticle
from .forms import OurCourseCreationForm, CourseArticleCreationForm
from django.views.generic import (ListView,
									CreateView,
									DetailView,
									UpdateView,
									DeleteView,
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


class CourseUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
	'''
	A CBV to update the course information
	'''
	model = OurCourse
	form_class = OurCourseCreationForm
	template_name = 'courses/course_info_update_view.html'
    
	def form_valid(self, form):
		form.instance.course_instructor = self.request.user
		return super().form_valid(form)

	def test_func(self):
		course = self.get_object()
		if self.request.user == course.course_instructor:
			return True
		return False

	def get_context_data(self, *args, **kwargs):
		context = super(CourseUpdateView, self).get_context_data(*args, **kwargs)
		context['title'] = 'Update-course'
		return context

class CourseDeletionView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
	'''
	A CBV to delete a course
	'''
	model = OurCourse
	success_url = '/'
	template_name = 'courses/course_deletion_confirm_view.html'

	def test_func(self):
		course = self.get_object()
		if self.request.user == course.course_instructor:
			return True
		return False


class CourseArticleCreationView(LoginRequiredMixin, CreateView):
	'''
	A CBV to manage the article creation to a course
	'''
	model = CourseArticle
	form_class = CourseArticleCreationForm
	template_name = 'course_articles/answer_create_page.html'


	def form_valid(self, form):
		form.instance.course_id = self.kwargs['pk']
		form.instance.article_author = self.request.user
		return super().form_valid(form)

	def test_func(self):
		course = self.get_object()
		if self.request.user == course.course_instructor and self.request.user.is_our_teacher:
			return True
		return False	

	def get_context_data(self, *args, **kwargs):
		context = super(CourseArticleCreationView, self).get_context_data(*args, **kwargs)
		context['title'] = f'{course.course_title} - Add-article'
		return context


class CourseArticleUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
	'''
	A CBV to update an article of a course
	'''
	model = CourseArticle
	form_class = CourseArticleCreationForm

	template_name = 'course_articles/course_article_update_view.html'

	def form_valid(self, form):
		return super().form_valid(form)

	def test_func(self):
		article = self.get_object()
		if self.request.user == article.article_author:
			return True
		return False

	def get_context_data(self, *args, **kwargs):
		context = super(CourseArticleUpdateView, self).get_context_data(*args, **kwargs)
		context['title'] = 'Update-article'
		return context


class CourseArticleDeletionView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
	'''
	A CBV to delete an article
	'''
	model = CourseArticle
	success_url = '/'
	template_name = 'course_articles/course_article_delete_view.html'

	def test_func(self):
		article = self.get_object()
		if self.request.user == article.article_author:
			return True
		return False

	def get_context_data(self, *args, **kwargs):
		context = super(CourseArticleDeletionView, self).get_context_data(*args, **kwargs)
		context['title'] = 'Delete-article'
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