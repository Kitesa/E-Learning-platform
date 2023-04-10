from django.urls import path, include
from .views import(
    HomePageView,
    )
app_name = "homepage"
urlpatterns = [
    path('',  HomePageView, name="homepage"),
]