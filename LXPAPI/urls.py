from django.urls import path, include
from lxpapiapp.lxpappApiViews import *
urlpatterns = [
    path('api/cto/', include('cto.urls')),
    path('api/cfo/', include('cfo.urls')),
    path('api/signup/', SignupAPIView.as_view(), name='api-signup'),
    path('api/login/', LoginAPI.as_view(), name='api-login'),
    path('api/change-password/', ChangePasswordAPIView.as_view(), name='api-change-password'),
    path('api/admin/view-users/', AdminViewUserList.as_view(), name='api-admin-view-user-list'),
    path('api/admin/user-log-details/<int:user_id>/', AdminViewUserLogDetailsAPIView.as_view(), name='api-user-log-details'),
    path('api/admin/user-activity-details/<int:user_id>/', AdminViewUserActivityDetailsAPIView.as_view(), name='api-user-activity-details'),
    path('api/admin/toggle-user-status/<int:user_id>/', AdminToggleUserStatusAPIView.as_view(), name='api-toggle-user-status'),
    path('api/delete-user/<int:user_id>/', DeleteUserAPIView.as_view(), name='api-delete-user'),
    path('api/user-profile/', UserProfileView.as_view(), name='api-user-profile'),
    path('api/user-info/', UserInfoView.as_view(), name='user-info'),
]