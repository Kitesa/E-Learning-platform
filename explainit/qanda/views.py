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


class QandaHomeView(ListView):
	'''
	A class based view to manage list of questions to be displayed
	'''
	model 			= Question
	template_name 	= 'qanda/qanda_home_page.html'

	def get_context_data(self, *args, **kwargs):
		user_questions = Question.objects.filter(author_id=self.request.user.pk)
		question_from_user_enrolled_same_course = Question.objects.all()
		suggested_questions = Question.objects.all()
		context = super(QandaHomeView, self).get_context_data(*args, **kwargs)
		context['title'] = "ExplainIT-Q&A"
		context['user_questions'] = user_questions
		context['suggested_questions'] = suggested_questions
		context['question_from_user_enrolled_same_course'] = question_from_user_enrolled_same_course
		return context

class QuestionDetailView(DetailView):
	'''
		A CBV that is used to show detail info about question
	'''
	model = Question
	context_object_name = 'question'
	template_name = 'qanda/question_detail_view.html'

	def get_context_data(self, *args, **kwargs):
		splited_course_name = self.get_object().title.split()
		related_questions = Question.objects.filter(Q(title__icontains=self.object.title) | Q(title=self.object.title) | Q(title__in=splited_course_name))
		context = super(QuestionDetailView, self).get_context_data(*args, **kwargs)
		context['title'] = self.get_object().title
		context['related_questions'] = related_questions
		context['splited_course_name'] = splited_course_name
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
		return super().form_valid(form)

	def get_context_data(self, *args, **kwargs):
		question = Question.objects.get(pk=self.kwargs['pk'])
		splited_course_name = question.title.split()
		related_questions = Question.objects.filter(Q(title__icontains=question.title) | Q(title=question.title) | Q(title__in=splited_course_name))
		answers = Answer.objects.filter(question_id=self.kwargs['pk'])
		context = super(AnswerCreationView, self).get_context_data(*args, **kwargs)
		context['title'] = 'Answers - ' + f'{question.title}'
		context['answers'] = answers
		context['related_questions'] = related_questions
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

	def test_func(self):
		Answer = self.get_object()
		if self.request.user == Answer.who_answered:
			return True
		return False

	def get_context_data(self, *args, **kwargs):
		context = super(AnswerDeletionView, self).get_context_data(*args, **kwargs)
		context['title'] = 'Delete-answer'
		return context