from django.urls import path,include
from django.contrib import admin
from lxpapp import views
from django.contrib.auth.views import LoginView
from django.contrib.auth import views as auth_views
urlpatterns = [
    
    path('admin/', admin.site.urls),
    path('login/', views.login, name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('social-auth/', include('social_django.urls', namespace='social')),
    path("", views.home, name='home'),
    path('cto/',include('cto.urls')),
    path('cfo/',include('cfo.urls')),
    path('learner/',include('learner.urls')),
    path('trainer/',include('trainer.urls')),
    path('aboutus', views.aboutus_view),
    path('contactus', views.contactus_view),
    path('afterlogin', views.afterlogin_view,name='afterlogin'),   

    path('adminclick', views.adminclick_view),
    path('adminlogin', LoginView.as_view(template_name='lxpapp/adminlogin.html'),name='adminlogin'),
    path('admin-dashboard', views.admin_dashboard_view,name='admin-dashboard'),
    path('admin-view-user', views.admin_view_user_view,name='admin-view-user'),
    path('update-user/<userfirstname>/<userlastname>/<userid>/<int:pk>', views.update_user_view,name='update-user'),
    path('active-user/<userid>/<int:pk>', views.active_user_view,name='active-user'),
    path('inactive-user/<int:pk>', views.inactive_user_view,name='inactive-user'),
    path('delete-user/<userid>/<int:pk>', views.delete_user_view,name='delete-user'),
]


