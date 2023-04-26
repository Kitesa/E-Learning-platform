from django.urls import path, include
from .views import (ArticleHomeView,
                        #QUESTIONS VIEW IMPORT
                        ArticleCreationView,
                        ArticleUpdateView,
                        ArticleDeletionView,

                        #LIKESDISLIKES
                        like_article,
                        dislike_article,

                        #ARTICLE-QUESTIONS
                        ArticleQuestionCreationView,
                        ArticleQuestionUpdateView,
                        ArticleQuestionDeletionView,
                        )

app_name = "articles"
urlpatterns = [
      path("", ArticleHomeView.as_view(), name="article-home-view"),

      #ARTICLES
      path('new/', ArticleCreationView.as_view(), name='article-creation-view'),
      path('<int:pk>/update', ArticleUpdateView.as_view(), name='article-update-view'),
      path('<int:pk>/delete', ArticleDeletionView.as_view(), name='article-deletion-view'),

      #ARTICLE QUESTIONS
      path('<int:pk>/new_question/', ArticleQuestionCreationView.as_view(), name='article-question-creation-view'),
      path('question/<int:pk>/update', ArticleQuestionUpdateView.as_view(), name='article-question-update-view'),
      path('question/<int:pk>/delete', ArticleQuestionDeletionView.as_view(), name='article-question-deletion-view'),
      
      #LIKES-DISLIKES
      path('<int:pk>/like/', like_article, name='likes'),
      path('<int:pk>/dis-like/', dislike_article, name='dislikes'),

]