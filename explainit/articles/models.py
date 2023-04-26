from django.db import models
from django.conf import settings
from accounts.models import Account
from django.urls import reverse
from ckeditor.fields import RichTextField
from datetime import datetime, timezone
from io import BytesIO
from django.core.files.storage import default_storage as storage
from django.core.files.base import ContentFile
from PIL import Image

def article_banner_image_upload_path(self, filename):
	'''
		A function that returns a file system path to which
		the platform should upload the article banner image
	'''
	return f'article_files/{self.author.username}/{self.article_title}/{"article_banner.jpeg"}'


class Article(models.Model):
	article_banner		= models.ImageField(upload_to=article_banner_image_upload_path)
	article_title 		= models.CharField(max_length = 100,
							error_messages = {"max_length":"Maximum length of 100"})
	article_content 	= RichTextField()
	date_published 		= models.DateTimeField(auto_now_add = True)
	date_updated 		= models.DateTimeField(auto_now = True)
	author 				= models.ForeignKey(settings.AUTH_USER_MODEL, 
    					on_delete=models.CASCADE)
	likes				= models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='likes')
	dislikes			= models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='dislikes')
	
	@property
	def total_likes(self):
		'''
		a function that returns total number of likes on article
		'''
		return f'{self.likes.count()}'

	@property
	def total_dislikes(self):
		'''
		a function that returns total number of dislikes on article
		'''
		return f'{self.dislikes.count()}'

	@property
	def date_difference(self):
		'''
		A function to manage the ages of the article
		'''
		now = datetime.now(timezone.utc)
		article_age = now - self.date_published

		return f'{article_age.days}'

	class Meta:
		ordering = ['-date_published',]

	def save(self, **kwargs):
		'''
			crop the article banner before uploading 
		'''
		super().save()
		if self.article_banner.url:
			img_read = storage.open(self.article_banner.name, "r")
			img = Image.open(img_read)
			if img.height > 800 or img.width > 400:
				output_size = (400, 800)
				imageBuffer = BytesIO()
				img.thumbnail(output_size)
				img = img.convert('RGB')
				img.save(imageBuffer, 'jpeg')

				self.article_banner.save(self.article_banner.name, ContentFile(imageBuffer.getvalue()))


	def __str__(self):
		return self.article_title

	def get_absolute_url(self):
		return reverse('articles:article-home-view')


class ArticleQuestion(models.Model):
	'''
	A db model to manage the questions to a article
	'''
	article 					= models.ForeignKey(Article, related_name='questions', on_delete=models.CASCADE)
	content 					= RichTextField()
	who_asked 					= models.ForeignKey(settings.AUTH_USER_MODEL, related_name='asker', on_delete=models.CASCADE)
	date_asked					= models.DateTimeField(auto_now_add=True)
	date_updated 				= models.DateTimeField(auto_now=True)


	class Meta:
		ordering = ['-date_asked',]

	def __str__(self):
		return f'questions to {self.article.article_title}'

	def get_absolute_url(self):
		return reverse('articles:article-question-creation-view', args=[self.article.pk])
