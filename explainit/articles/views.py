from django.shortcuts import render, get_object_or_404, redirect
from .models import Article, ArticleQuestion
from django.views.generic import (ListView,
									CreateView,
									DetailView,
									UpdateView,
									DeleteView,
									)
from django.contrib.auth.mixins import (LoginRequiredMixin,
										UserPassesTestMixin,
										)
from .forms import (ArticleCreationForm,
					ArticleQuestionCreationForm,
					)
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.cache import cache
from django.urls import reverse

class ArticleHomeView(ListView):
	'''
	A class based view to manage list of articles to be displayed
	'''
	model 			= Article
	template_name 	= 'articles/article_home_page.html'

	def get_context_data(self, *args, **kwargs):
		user_articles = Article.objects.filter(author_id=self.request.user.pk)
		suggested_articles = Article.objects.all()
		
		if cache.get('user_articles') and cache.get('suggested_articles'):
			user_articles = cache.get('user_articles')
			suggested_articles = cache.get('suggested_articles')
		else:
			cache.set('user_articles', user_articles)
			cache.set('suggested_articles', suggested_articles)
			user_articles = cache.get('user_articles')
			suggested_articles = cache.get('suggested_articles')
		context = super(ArticleHomeView, self).get_context_data(*args, **kwargs)
		context['title'] = "ExplainIT-Articles"
		context['user_articles'] = user_articles
		context['suggested_articles'] = suggested_articles
		return context


class ArticleCreationView(LoginRequiredMixin, CreateView):
	'''
	A CBV used to create an article
	'''
	model 			= Article
	form_class 		= ArticleCreationForm
	template_name 	= 'articles/article_create_page.html'
    

	def form_valid(self, form):
		form.instance.author = self.request.user
		messages.success(self.request, "Article published successfully")
		return super().form_valid(form)

	def get_context_data(self, *args, **kwargs):
		context = super(ArticleCreationView, self).get_context_data(*args, **kwargs)
		context['title'] = 'Add-article'
		return context


class ArticleUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
	'''
	A CBV to update an article
	'''
	model = Article
	form_class = ArticleCreationForm
	template_name = 'articles/article_update_view.html'
    
	def form_valid(self, form):
		form.instance.author = self.request.user
		messages.success(self.request, "Article updated successfully")
		return super().form_valid(form)

	def test_func(self):
		Article = self.get_object()
		if self.request.user == Article.author:
			return True
		return False

	def get_context_data(self, *args, **kwargs):
		context = super(ArticleUpdateView, self).get_context_data(*args, **kwargs)
		context['title'] = 'Update-article'
		return context


class ArticleDeletionView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
	'''
	A CBV to delete a question
	'''
	model = Article
	template_name = 'articles/article_delete_page.html'

	def get_success_url(self):
		'''
		where to redirect the user after successful deletion of the course
		'''
		course = self.get_object()
		return reverse( 'articles:article-home-view')

	def form_valid(self, form):
		messages.success(self.request, "Article deleted successfully")
		return super().form_valid(form)	

	def test_func(self):
		Article = self.get_object()
		if self.request.user == Article.author:
			return True
		return False

@login_required
def like_article(request, pk):
    if request.method == 'GET':
        user = request.user
        article = get_object_or_404(Article, pk=pk)

        if article.likes.filter(id=user.id).exists():
            article.likes.remove(user)
            message=messages.success(request,f'You removed your likes from the question')
        else:
            article.likes.add(user)
            message =messages.success(request, f'You liked the article')
            return redirect(request.META.get('HTTP_REFERER'))
    return redirect(request.META.get('HTTP_REFERER'))

@login_required
def dislike_article(request, pk):
    if request.method == 'GET':
        user = request.user
        article = get_object_or_404(Article, pk=pk)

        if article.dislikes.filter(id=user.id).exists():
            article.dislikes.remove(user)
            message=messages.success(request,f'You removed your dis-likes from the question')
        else:
            article.dislikes.add(user)
            message =messages.success(request, f'You disliked the article')
            return redirect(request.META.get('HTTP_REFERER'))
    return redirect(request.META.get('HTTP_REFERER'))


class ArticleQuestionCreationView(LoginRequiredMixin, CreateView):
	'''
	A CBV used to create question on an article
	'''
	model 			= ArticleQuestion
	form_class 		= ArticleQuestionCreationForm
	template_name 	= 'article_questions/article_question_create_page.html'
    

	def form_valid(self, form):
		form.instance.article_id = self.kwargs['pk']
		form.instance.who_asked = self.request.user
		messages.success(self.request, "Question added successfully")
		return super().form_valid(form)

	def get_context_data(self, *args, **kwargs):
		article = Article.objects.get(pk=self.kwargs['pk'])
		context = super(ArticleQuestionCreationView, self).get_context_data(*args, **kwargs)
		context['title'] = 'Add-question'
		context['article'] = article
		return context


class ArticleQuestionUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
	'''
	A CBV to update a question on an article
	'''
	model = ArticleQuestion
	form_class = ArticleQuestionCreationForm
	template_name = 'article_questions/article_question_update_view.html'
	
	def test_func(self):
		article_question = self.get_object()
		if self.request.user == article_question.who_asked:
			return True
		return False

	def form_valid(self, form):
		messages.success(self.request, "Question updated successfully")
		return super().form_valid(form)

	def get_context_data(self, *args, **kwargs):
		context = super(ArticleQuestionUpdateView, self).get_context_data(*args, **kwargs)
		context['title'] = 'Update-article'
		return context


class ArticleQuestionDeletionView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
	'''
	A CBV to delete an article question
	'''
	model = ArticleQuestion

	template_name = 'article_questions/article_question_delete_page.html'

	def get_success_url(self):
		'''
		where to redirect the user after successful deletion of the course
		'''
		question = self.get_object()
		return reverse( 'articles:article-question-creation-view', args=[question.article.pk])

	def form_valid(self, form):
		messages.success(self.request, "Question deleted successfully")
		return super().form_valid(form)	

	def test_func(self):
		question = self.get_object()
		if self.request.user == question.who_asked:
			return True
		return False
	
	def get_context_data(self, *args, **kwargs):
		question = self.get_object()
		context = super(ArticleQuestionDeletionView, self).get_context_data(*args, **kwargs)
		context['title'] = 'Delete-question'
		context['question'] = question
		return context
