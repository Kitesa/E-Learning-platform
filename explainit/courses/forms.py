from django import forms
from .models import OurCourse

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
		fields  	= "__all__"