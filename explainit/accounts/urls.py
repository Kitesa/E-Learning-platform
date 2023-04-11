from django.urls import path, include
from django.contrib.auth import views as auth_views
from . views import (
            AccountCreationPageView,
            TermsOfServiceListView,

            #PROFILE
            UserProfileHomeView,
    )

app_name = "accounts"
urlpatterns = [
    path('register/', AccountCreationPageView, name='register-page'),
    path('terms-of-serives/', TermsOfServiceListView.as_view(), name='terms-of-service-page'),
    path('login/', auth_views.LoginView.as_view(template_name='accounts/account_login_page.html'), name='login-page'),
    path('logout/', auth_views.LogoutView.as_view(template_name='accounts/account_logout_page.html'), name='logout-page'),
    #PASSWORD
    path('password-reset/', auth_views.PasswordResetView.as_view(template_name='password/password_reset.html'), name='password_reset'),
    path('password-reset/done/',auth_views.PasswordResetDoneView.as_view(template_name='password/password_reset_done.html'), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name='password/password_reset_confirm.html'), name='password_reset_confirm'),
    path('password-reset-complete/',auth_views.PasswordResetCompleteView.as_view(template_name='password/password_reset_complete.html'), name='password_reset_complete'),

    #ACCOUNT_PROFILE
    path("profile/", UserProfileHomeView, name="user-profile-home-view"),

]   