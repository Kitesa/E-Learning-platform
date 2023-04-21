from django import forms
from .models import Question, Answer

class QuestionCreationForm(forms.ModelForm):
	'''
		A model form to be rendered on template
		to create a new question
	'''
	class Meta:
		model 		= Question
		fields  	= ['question_title', 'question_category', 'question_content']

class AnswerCreationForm(forms.ModelForm):
	class Meta:
		model 		= Answer
		fields   	= ['content',]
