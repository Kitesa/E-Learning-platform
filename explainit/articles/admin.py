from django.contrib import admin
from .models import (Article,
					ArticleQuestion)

admin.site.register(Article)
admin.site.register(ArticleQuestion)