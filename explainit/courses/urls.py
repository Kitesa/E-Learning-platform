from django.urls import path, include
from .views import (OurCourseHomeView,
				OurCourseCreateView,
				CourseDetailView,

				enroll_courses,
					)

app_name = "courses"
urlpatterns = [
      path("", OurCourseHomeView.as_view(), name="course-home-view"),
      path("<str:pk>/create/", OurCourseCreateView.as_view(), name="course-create-view"),
      path("<str:pk>/", CourseDetailView.as_view(), name="course-detail-view"),

      path('<int:pk>/enroll/', enroll_courses, name='enroll'),
]