from django.db import models
from django.conf import settings
from accounts.models import Account
from django.urls import reverse
from ckeditor.fields import RichTextField

class QuestionCategory(models.Model):
	category_name = models.CharField(max_length=30)

	def __str__(self):
		return self.category_name

class Question(models.Model):
	question_title 		= models.CharField(max_length = 100,
							error_messages = {"max_length":"Maximum length of 100"})
	question_category 	= models.ForeignKey(QuestionCategory, on_delete=models.CASCADE)
	question_content 	= RichTextField()
	date_asked 			= models.DateTimeField(auto_now_add = True)
	date_updated 		= models.DateTimeField(auto_now = True)
	author 				= models.ForeignKey(settings.AUTH_USER_MODEL, 
    					on_delete=models.CASCADE)

	class Meta:
		ordering = ['-date_asked',]

	def __str__(self):
		return self.question_title

	def get_absolute_url(self):
		return reverse('qanda:qanda-home-view')


class Answer(models.Model):
	'''
	A db model to manage the answers to a questiuon
	'''
	question = models.ForeignKey(Question, related_name='answers', on_delete=models.CASCADE)
	content= RichTextField(verbose_name="Your answer",)
	who_answered = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='who_answered', on_delete=models.CASCADE)
	date_answered = models.DateTimeField(auto_now_add=True)
	date_updated = models.DateTimeField(auto_now=True)


	class Meta:
		ordering = ['-date_answered',]

	def __str__(self):
		return f'answers to {self.question.content}'

	def get_absolute_url(self):
		return reverse('qanda:question-detail-view', args=[self.question.pk])
