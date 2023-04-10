from django.urls import path, include
from django.contrib.auth import views as auth_views
from . views import (
            AccountCreationPageView,
    )

app_name = "accounts"
urlpatterns = [
    path('register/', AccountCreationPageView, name='register-page'),
    path('logout/', auth_views.LogoutView.as_view(template_name='accounts/account_logout_page.html'), name='logout-page'),
]   