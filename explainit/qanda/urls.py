from django.urls import path, include
from .views import (QandaHomeView,
                        #QUESTIONS VIEW IMPORT
                        QuestionCreationView,
                        QuestionUpdateView,
                        QuestionDeletionView,

                        #ANSWER VIEW IMPORT
                        AnswerCreationView,
                        AnswerUpdateView,
                        AnswerDeletionView,

                        #REASKS
                        reask_question,
                        )

app_name = "qanda"
urlpatterns = [
      path("", QandaHomeView.as_view(), name="qanda-home-view"),

      #QUESTIONS
      path('new/', QuestionCreationView.as_view(), name='question-creation-view'),
      path('<int:pk>/update', QuestionUpdateView.as_view(), name='question-update-view'),
      path('<int:pk>/delete', QuestionDeletionView.as_view(), name='question-deletion-view'),

      #ANSWERS
      path('answer/<int:pk>/add_answer', AnswerCreationView.as_view(), name='answer-creation-view'),
      path('answer/<int:pk>/update', AnswerUpdateView.as_view(), name='answer-update-view'),
      path('answer/<int:pk>/delete', AnswerDeletionView.as_view(), name='answer-deletion-view'),

      #REASKS
      path('<int:pk>/enroll/', reask_question, name='reask'),
]