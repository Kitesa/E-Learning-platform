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
