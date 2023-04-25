from django.urls import path, include
from .views import (ArticleHomeView,
                        #QUESTIONS VIEW IMPORT
                        ArticleCreationView,
                        ArticleUpdateView,
                        ArticleDeletionView,

                        #LIKES
                        like_article,
                        )

app_name = "articles"
urlpatterns = [
      path("", ArticleHomeView.as_view(), name="article-home-view"),

      #ARTICLES
      path('new/', ArticleCreationView.as_view(), name='article-creation-view'),
      path('<int:pk>/update', ArticleUpdateView.as_view(), name='article-update-view'),
      path('<int:pk>/delete', ArticleDeletionView.as_view(), name='article-deletion-view'),

      #LIKES
      path('<int:pk>/like/', like_article, name='likes'),
]