from django.shortcuts import render, get_object_or_404, redirect
from .models import Question, Answer
from django.views.generic import (ListView,
									CreateView,
									DetailView,
									UpdateView,
									DeleteView,
									)
from django.contrib.auth.mixins import (LoginRequiredMixin,
										UserPassesTestMixin,
										)
from .forms import (QuestionCreationForm,
					AnswerCreationForm,
					)
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.cache import cache
from django.urls import reverse

class QandaHomeView(ListView):
	'''
	A class based view to manage list of questions to be displayed
	'''
	model 			= Question
	template_name 	= 'qanda/qanda_home_page.html'

	def get_context_data(self, *args, **kwargs):
		user_questions = Question.objects.filter(author_id=self.request.user.pk)
		suggested_questions = Question.objects.all()
		filtered_questions = user_questions | suggested_questions
		if cache.get('filtered_questions'):
			user_questions = cache.get('user_questions')
			filtered_questions = cache.get('filtered_questions')
		else:
			cache.set('user_questions', user_questions)
			cache.set('filtered_questions', filtered_questions)
			user_questions = cache.get('user_questions')
			filtered_questions = cache.get('filtered_questions')
		context = super(QandaHomeView, self).get_context_data(*args, **kwargs)
		context['title'] = "ExplainIT-Q&A"
		context['user_questions'] = user_questions
		context['filtered_questions'] = filtered_questions
		return context


class QuestionCreationView(LoginRequiredMixin, CreateView):
	'''
	A CBV used to create a question
	'''
	model 			= Question
	form_class 		= QuestionCreationForm
	template_name 	= 'qanda/question_create_page.html'
    

	def form_valid(self, form):
		form.instance.author = self.request.user
		messages.success(self.request, "Question created successfully")
		return super().form_valid(form)

	def get_context_data(self, *args, **kwargs):
		context = super(QuestionCreationView, self).get_context_data(*args, **kwargs)
		context['title'] = 'Add-question'
		return context

@login_required
def reask_question(request, pk):
    if request.method == 'GET':
        user = request.user
        question = get_object_or_404(Question, pk=pk)

        if question.reasks.filter(id=user.id).exists():
            question.reasks.remove(user)
            message=messages.success(request,f'You removed your reasks from the question')
        else:
            question.reasks.add(user)
            message =messages.success(request, f'You reasked the question')
            return redirect(request.META.get('HTTP_REFERER'))
    return redirect(request.META.get('HTTP_REFERER'))

class QuestionUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
	'''
	A CBV to update the question
	'''
	model = Question
	form_class = QuestionCreationForm
	template_name = 'qanda/question_update_view.html'
    
	def form_valid(self, form):
		form.instance.author = self.request.user
		messages.success(self.request, "Question updated successfully")
		return super().form_valid(form)

	def test_func(self):
		Question = self.get_object()
		if self.request.user == Question.author:
			return True
		return False

	def get_context_data(self, *args, **kwargs):
		context = super(QuestionUpdateView, self).get_context_data(*args, **kwargs)
		context['title'] = 'Update-question'
		return context


class QuestionDeletionView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
	'''
	A CBV to delete a question
	'''
	model = Question
	success_url = '/'
	template_name = 'qanda/question_delete_page.html'
	
	def get_success_url(self):
		'''
		where to redirect the user after successful deletion of the question
		'''
		return reverse( 'qanda:qanda-home-view')
			
	def form_valid(self, form):
		messages.success(self.request, "Question deleted successfully")
		return super().form_valid(form)	

	def test_func(self):
		Question = self.get_object()
		if self.request.user == Question.author:
			return True
		return False


class AnswerCreationView(LoginRequiredMixin, CreateView):
	'''
	A CBV to manage the answer creation to a question
	'''
	model = Answer
	form_class = AnswerCreationForm
	template_name = 'answers/answer_create_page.html'


	def form_valid(self, form):
		form.instance.question_id = self.kwargs['pk']
		form.instance.who_answered = self.request.user
		messages.success(self.request, "Answer added successfully")
		return super().form_valid(form)

	def get_context_data(self, *args, **kwargs):
		question = Question.objects.get(pk=self.kwargs['pk'])
		if cache.get('question'):
			question = cache.get('question')
		else:
			cache.set('question', question)
			question = cache.get('question')
		context = super(AnswerCreationView, self).get_context_data(*args, **kwargs)
		context['title'] = 'Answers to - ' + f'{question.question_title}'
		context['question'] = question
		return context


class AnswerUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
	'''
	A CBV to update an answer to a question
	'''
	model =Answer
	form_class = AnswerCreationForm

	template_name = 'answers/answer_update_page.html'

	def form_valid(self, form):
		messages.success(self.request, "Answer updated successfully")
		return super().form_valid(form)

	def test_func(self):
		Answer = self.get_object()
		if self.request.user == Answer.who_answered:
			return True
		return False

	def get_context_data(self, *args, **kwargs):
		context = super(AnswerUpdateView, self).get_context_data(*args, **kwargs)
		context['title'] = 'Update-answer'
		return context


class AnswerDeletionView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
	'''
	A CBV to delete an answer
	'''
	model = Answer
	success_url = '/'
	template_name = 'answers/answer_delete_page.html'

	def form_valid(self, form):
		messages.success(self.request, "Answer deleted successfully")
		return super().form_valid(form)


	def test_func(self):
		Answer = self.get_object()
		if self.request.user == Answer.who_answered:
			return True
		return False

	def get_context_data(self, *args, **kwargs):
		context = super(AnswerDeletionView, self).get_context_data(*args, **kwargs)
		context['title'] = 'Delete-answer'
		return context