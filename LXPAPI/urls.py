from django.urls import include, path, re_path

from lxpapiapp.lxpappApiViews import *
from django.contrib.auth import views as auth_views
urlpatterns = [
    path("login/", LoginPage.as_view(), name="login"),
    path("api/v1/auth/", include("dj_rest_auth.urls")),
    re_path(r"^api/v1/auth/accounts/", include("allauth.urls")),
    path("api/v1/auth/registration/", include("dj_rest_auth.registration.urls")),
    path("api/v1/auth/google/", GoogleLogin.as_view(), name="google_login"),
    path(
        "api/v1/auth/google/callback/",
        GoogleLoginCallback.as_view(),
        name="google_login_callback", 
    ),
    path('complete/google/', google_complete, name='google_complete'),
    path('api/cto/', include('cto.urls')),
    path('api/cfo/', include('cfo.urls')),
    path('api/staff/', include('staff.urls')), 
    path('api/signup/', SignupAPIView.as_view(), name='api-signup'),
    path('api/loginuser/', LoginAPI.as_view(), name='api-login-user'),
    path('logout/', custom_logout, name='logout'),
    path('api/change-password/', ChangePasswordAPIView.as_view(), name='api-change-password'),
    path('api/admin/view-users/', AdminViewUserList.as_view(), name='api-admin-view-user-list'),
    path('api/admin/user-log-details/<int:user_id>/', AdminViewUserLogDetailsAPIView.as_view(), name='api-user-log-details'),
    path('api/admin/user-activity-details/<int:user_id>/', AdminViewUserActivityDetailsAPIView.as_view(), name='api-user-activity-details'),
    path('api/admin/toggle-user-status/<int:user_id>/', AdminToggleUserStatusAPIView.as_view(), name='api-toggle-user-status'),
    path('api/delete-user/<int:user_id>/', DeleteUserAPIView.as_view(), name='api-delete-user'),
    path('api/user-profile/', UserProfileView.as_view(), name='api-user-profile'),
    path('api/user-info/', UserInfoView.as_view(), name='user-info'),

]