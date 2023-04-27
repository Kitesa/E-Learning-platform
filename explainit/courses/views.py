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
from django.urls import reverse
from django.core.cache import cache
from hitcount.views import HitCountDetailView

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
		our_courses = OurCourse.objects.all()
		if cache.get('our_courses'):
			our_courses = cache.get('our_courses')
		else:
			cache.set('our_courses', our_courses)
			our_courses = cache.get('our_courses')
		context = super(OurCourseHomeView, self).get_context_data(*args, **kwargs)
		context['title'] = "ExplainIT-Courses"
		context['our_courses'] = our_courses
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
		messages.success(self.request, 'Course created successfully')
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
		'''
		who can create a course
		'''
		if self.request.user.is_our_teacher or self.request.user.is_admin:
			return True
		return False

class CourseDetailView(HitCountDetailView, DetailView):
	model 			= OurCourse
	template_name	= 'courses/our_course_detail_view.html'
	count_hit		= True
	def get_context_data(self, *args, **kwargs):
		'''
		what should be sent to course detail view page
		'''
		course 	= self.get_object()
		if cache.get('course'):
			course = cache.get('course')
		else:
			cache.set('course', course)
			course = cache.get('course')

		context = super(CourseDetailView, self).get_context_data(*args, **kwargs)
		context['title'] = course.course_title
		context['course'] = course
		return context


class CourseUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
	'''
	A CBV to update the course information
	'''
	model = OurCourse
	form_class = OurCourseCreationForm
	template_name = 'courses/course_info_update_view.html'
    
	def form_valid(self, form):
		'''
		What will happen if the form is valid
		'''
		form.instance.course_instructor = self.request.user
		messages.success(self.request, 'Course updated successfully')
		return super().form_valid(form)

	def test_func(self):
		'''
		who can update a course
		'''
		course = self.get_object()
		if self.request.user == course.course_instructor:
			return True
		return False

	def get_context_data(self, *args, **kwargs):
		'''
		what should be sent to course update page
		'''
		context = super(CourseUpdateView, self).get_context_data(*args, **kwargs)
		context['title'] = 'Update-course'
		return context

class CourseDeletionView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
	'''
	A CBV to delete a course
	'''
	model = OurCourse
	template_name = 'courses/course_deletion_confirm_view.html'

	def get_success_url(self):
		'''
		where to redirect the user after successful deletion of the course
		'''
		course = self.get_object()
		return reverse( 'courses:course-home-view')

	def form_valid(self, form):
		'''
		What will happen if the form is valid
		'''
		messages.success(self.request, 'Course deleted successfully')
		return super().form_valid(form)

	def test_func(self):
		'''
		who can delete a course
		'''
		course = self.get_object()
		if self.request.user == course.course_instructor:
			return True
		return False

	def get_context_data(self, *args, **kwargs):
		'''
		what should be sent to course deletion page
		'''
		course = OurCourse.objects.get(pk=self.kwargs['pk'])
		context = super(CourseDeletionView, self).get_context_data(*args, **kwargs)
		context['title'] = f'{course.course_title} - delete'
		context['course'] = course
		return context


class CourseArticleCreationView(LoginRequiredMixin, CreateView):
	'''
	A CBV to manage the article creation to a course
	'''
	model = CourseArticle
	form_class = CourseArticleCreationForm
	template_name = 'course_articles/course_article_creation_view.html'


	def form_valid(self, form):
		'''
		What will happen if the form is valid
		'''
		form.instance.course_id = self.kwargs['pk']
		form.instance.article_author = self.request.user
		messages.success(self.request, 'Article added successfully')
		return super().form_valid(form)

	def test_func(self):
		'''
		who can create an article
		'''
		course = self.get_object()
		if self.request.user == course.course_instructor and self.request.user.is_our_teacher:
			return True
		return False	

	def get_context_data(self, *args, **kwargs):
		'''
		what should be sent to article craetion page
		'''
		course = OurCourse.objects.get(pk=self.kwargs['pk'])
		context = super(CourseArticleCreationView, self).get_context_data(*args, **kwargs)
		context['title'] = f'{course.course_title} - Add-article'
		context['course'] = course
		return context


class CourseArticleUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
	'''
	A CBV to update an article of a course
	'''
	model = CourseArticle
	form_class = CourseArticleCreationForm

	template_name = 'course_articles/course_article_update_view.html'

	def form_valid(self, form):
		'''
		What will happen if the form is valid
		'''
		messages.success(self.request, 'Article updated successfully')
		return super().form_valid(form)

	def test_func(self):
		'''
		who can update an article
		'''
		article = self.get_object()
		if self.request.user == article.course.course_instructor:
			return True
		return False

	def get_context_data(self, *args, **kwargs):
		'''
		what should be sent to the article update page
		'''
		context = super(CourseArticleUpdateView, self).get_context_data(*args, **kwargs)
		context['title'] = 'Update-article'
		return context


class CourseArticleDeletionView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
	'''
	A CBV to delete an article
	'''
	model = CourseArticle
	template_name = 'course_articles/course_article_deletion_view.html'

	def get_success_url(self):
		'''
		Where to redirect the user after successful deletion
		of an article
		'''
		article = self.get_object()
		return reverse( 'courses:course-detail-view', args=[article.course.pk])

	def form_valid(self, form):
		'''
		What will happen if the form is valid
		'''
		messages.success(self.request, 'Article deleted successfully')
		return super().form_valid(form)


	def test_func(self):
		'''
		who can delete an article
		'''
		article = self.get_object()
		if self.request.user == article.course.course_instructor:
			return True
		return False

	def get_context_data(self, *args, **kwargs):
		'''
		what should be sent to the deletion page
		'''
		article = CourseArticle.objects.get(pk=self.kwargs['pk'])
		context = super(CourseArticleDeletionView, self).get_context_data(*args, **kwargs)
		context['title'] = 'Delete-article'
		context['article'] = article
		return context


@login_required
def enroll_courses(request, pk):
	'''
	enroll or uneroll course
	'''
	if request.method == 'GET':
		user = request.user
		course = get_object_or_404(OurCourse, pk=pk)

		if course.students.filter(id=user.id).exists():
			#user has already enrolled the course
			#remove students from enrolled student list
			course.students.remove(user)
			message=messages.success(request,f'You stopped learning {course.course_title}')
		else:
			course.students.add(user)
			message =messages.success(request, f'You enrolled {course.course_title}')
			total_students = {'total_students':course.total_students}
			return redirect(request.META.get('HTTP_REFERER'))
	return redirect(request.META.get('HTTP_REFERER'))

class CourseStudentListView(DetailView):
	model 			= OurCourse
	template_name	= 'courses/course_student_list_view.html'

	def get_context_data(self, *args, **kwargs):
		'''
		what should be sent to course student list page
		'''
		course 	= self.get_object()

		context = super(CourseStudentListView, self).get_context_data(*args, **kwargs)
		context['title'] = f'{course.course_title}-Students'
		context['course'] = course
		return context