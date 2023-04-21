from django.contrib import admin
from .models import (QuestionCategory, 
					Question,
					Answer,
					)

admin.site.register(QuestionCategory)
admin.site.register(Question)
admin.site.register(Answer)