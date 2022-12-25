from django.urls import path,include
from django.contrib import admin
from lxpapp import views
from django.contrib.auth.views import LogoutView,LoginView
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
    #path('logout', LogoutView.as_view(template_name='lxpapp/logout.html'),name='logout'),
    path('aboutus', views.aboutus_view),
    path('contactus', views.contactus_view),
    path('afterlogin', views.afterlogin_view,name='afterlogin'),
    path('syncyoutube', views.syncyoutube_view,name='syncyoutube'),
    path('syncyoutube-start', views.syncyoutube_start_view,name='syncyoutube-start'),

    path('adminclick', views.adminclick_view),
    path('adminlogin', LoginView.as_view(template_name='lxpapp/adminlogin.html'),name='adminlogin'),
    path('admin-dashboard', views.admin_dashboard_view,name='admin-dashboard'),

    path('admin-view-user', views.admin_view_user_view,name='admin-view-user'),
    path('active-user/<userid>/<int:pk>', views.active_user_view,name='active-user'),
    path('inactive-user/<int:pk>', views.inactive_user_view,name='inactive-user'),
    path('admin-update-course/<int:pk>', views.admin_update_course_view,name='admin-update-course'),
    path('admin-mark-usertype/<int:pk>', views.admin_mark_usertype_view,name='admin-mark-usertype'),
    
 
]

