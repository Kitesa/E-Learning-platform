from django.urls import path, include
from django.contrib.auth import views as auth_views
from . views import (
            AccountCreationPageView,
            TermsOfServiceListView,
            AccountActivationView,

            #PROFILE
            UserProfileHomeView,
            UpdateUserProfile,

            #PROFILE PICTURE
            ProfilePicUpdateView,

            #ACCOUNT DETAIL
            AccountDetailView,

            #ACCOUNT FOLLOWERS
            followunfollow,
    )

app_name = "accounts"
urlpatterns = [
    path('register/', AccountCreationPageView, name='register-page'),
    path('activate/<uidb64>/<token>', AccountActivationView, name='activate-account'),
    path('terms-of-serives/', TermsOfServiceListView.as_view(), name='terms-of-service-page'),
    path('login/', auth_views.LoginView.as_view(template_name='accounts/account_login_page.html'), name='login-page'),
    path('logout/', auth_views.LogoutView.as_view(template_name='accounts/account_logout_page.html'), name='logout-page'),

    #ACCOUNT_PROFILE
    path("profile/", UserProfileHomeView, name="user-profile-home-view"),
    path("profile/update/", UpdateUserProfile, name="user-profile-update-view"),

    #PROFILE PICTURE
    path("profile/<int:pk>/update_profile_picture/", ProfilePicUpdateView.as_view(), name="user-profile-pic-update-view"),

    #ACCOUNT DETAIL
    path("profile/<int:pk>/", AccountDetailView.as_view(), name="account-detail-view"),

    #ACCOUNT FOLLOWERS
    path("profile/<int:pk>/follow", followunfollow, name="account-follow-unfollow"),

    

]   