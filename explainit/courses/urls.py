from django.urls import path, include
from .views import (OurCourseHomeView,
					OurCourseCreateView,
					CourseDetailView,
					enroll_courses,
					CourseUpdateView,
					CourseDeletionView,
					CourseStudentListView,

					#COURSE ARTICLE
					CourseArticleCreationView,
					CourseArticleUpdateView,
					CourseArticleDeletionView,

					)

app_name = "courses"
urlpatterns = [
	#COURSES
  	path("", OurCourseHomeView.as_view(), name="course-home-view"),
  	path("create/", OurCourseCreateView.as_view(), name="course-create-view"),
  	path("<str:pk>/update", CourseUpdateView.as_view(), name="course-update-view"),
  	path("<str:pk>/delete", CourseDeletionView.as_view(), name="course-deletion-view"),
  	path("<str:pk>/", CourseDetailView.as_view(), name="course-detail-view"),
  	path('<int:pk>/enroll', enroll_courses, name='enroll'),
  	path('<int:pk>/students', CourseStudentListView.as_view(), name='course-students'),
  	#COURSE ARTICLES
  	path("<str:pk>/add_article", CourseArticleCreationView.as_view(), name="article-creation-view"),
  	path("<str:pk>/update_article", CourseArticleUpdateView.as_view(), name="article-update-view"),
  	path("<str:pk>/delete_article", CourseArticleDeletionView.as_view(), name="article-delete-view"),
  	
  
]