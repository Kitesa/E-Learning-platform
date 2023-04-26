from django import forms
from .models import Article, ArticleQuestion

class ArticleCreationForm(forms.ModelForm):
	'''
		A model form to be rendered on template
		to create a new article
	'''
	class Meta:
		model 		= Article
		fields  	= ['article_banner', 'article_title', 'article_content']


class ArticleQuestionCreationForm(forms.ModelForm):
	'''
		A model form to be rendered on template
		to create a new article
	'''
	class Meta:
		model 		= ArticleQuestion
		fields  	= ['content', ]



