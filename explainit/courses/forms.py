from django import forms
from .models import OurCourse, CourseArticle

class OurCourseCreationForm(forms.ModelForm):
	'''
		A model form to be rendered on template
		to create a new course
	'''
	class Meta:
		model 		= OurCourse
		fields  	= ['course_title', 'course_description', 'course_poster']

class OurCourseUpdateForm(forms.ModelForm):
	'''
		A model form to be rendered on template
		to update a course information
	'''
	class Meta:
		model 		= OurCourse
		fields  	= ['course_title', 'course_description', 'course_poster']


class CourseArticleCreationForm(forms.ModelForm):
	'''
		A model form to be rendered on template
		to create a course article 
	'''
	class Meta:
		model 		= CourseArticle
		fields  	= ['article_content', 'article_identity_number']


