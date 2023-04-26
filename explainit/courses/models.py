from django.db import models
from django.conf import settings
from PIL import Image
from ckeditor.fields import RichTextField 
from django.conf import settings
from django.urls import reverse
from io import BytesIO
from django.core.files.storage import default_storage as storage
from django.core.files.base import ContentFile

def course_poster_image_upload_path(self, filename):
	'''
		A function that returns a file system path to which
		the platform should upload the course poster image
	'''
	return f'course_files/{self.course_instructor.username}/{self.course_title}/{"course_poster.jpeg"}'


class OurCourse(models.Model):
	'''
	 A DB model to hold the course 
	'''
	course_title 			= models.CharField(max_length=254)
	course_instructor		= models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="courses", null=True)
	is_free					= models.BooleanField(default=False)
	is_paid					= models.BooleanField(default=False)
	course_description 		= RichTextField()
	course_poster	 		= models.ImageField(upload_to=course_poster_image_upload_path, verbose_name= "Course poster" )
	is_approved 			= models.BooleanField(default=False)
	publish 				= models.BooleanField(default=False)
	students 				= models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='students', blank=True)
	date_created			= models.DateTimeField(auto_now_add=True, null=True)
	date_updated			= models.DateTimeField(auto_now=True, null=True)

	@property
	def total_students(self):
		return self.students.count()

	def __str__(self):
		'''
		String representation of the model
		'''
		return f'{self.course_title}'

	def get_absolute_url(self):
		'''
			redirect the user after successfull 
			creation of course
		'''
		return reverse('courses:course-detail-view', args=[self.pk])


	def save(self, **kwargs):
		'''
			crop the course poster before uploading 
		'''
		super().save()
		if self.course_poster.url:
			img_read = storage.open(self.course_poster.name, "r")
			img = Image.open(img_read)
			if img.height > 600 or img.width > 400:
				output_size = (400, 600)
				imageBuffer = BytesIO()
				img.thumbnail(output_size)
				img = img.convert('RGB')
				img.save(imageBuffer, 'jpeg')

				self.course_poster.save(self.course_poster.name, ContentFile(imageBuffer.getvalue()))


	def delete(self, using=None, keep_parents=False):
		'''
		 delete the course poster from file system if
		 the course is deleted
		 '''
		self.course_poster.storage.delete(self.course_poster.name)
		super().delete()


class CourseArticle(models.Model):
	course 				= models.ForeignKey(OurCourse, related_name='articles', on_delete=models.CASCADE, blank=True, null=True)
	article_content		= RichTextField(blank=True, null=True)
	date_created 		= models.DateTimeField(auto_now_add=True, blank=True, null=True)
	article_identity_number = models.IntegerField(null=True)
	add_options_to_this_article = models.BooleanField(default=1)

	class Meta:
		ordering = ['article_identity_number', ]

	def __str__(self):
		return "Articles under" + str(self.course.course_title) + " course by " + str(self.course.course_instructor.full_name)

	def get_absolute_url(self):
		return reverse('courses:course-detail-view', args=[self.course.pk])

