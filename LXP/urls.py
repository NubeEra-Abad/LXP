from django.urls import path,include
from django.contrib import admin
from lxpapp import views
from django.contrib.auth.views import LoginView
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static


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
    path('indexpage', views.afterlogin_view,name='indexpage'),   

    path('adminclick', views.adminclick_view),
    path('userlogin', LoginView.as_view(template_name='lxpapp/users/userlogin.html'),name='userlogin'),
    path('admin-dashboard', views.admin_dashboard_view,name='admin-dashboard'),
    path('admin-view-user-list', views.admin_view_user_list_view,name='admin-view-user-list'),
    path('admin-view-user-grid', views.admin_view_user_grid_view,name='admin-view-user-grid'),
    path('update-user/<userfirstname>/<userlastname>/<userid>/<int:pk>', views.update_user_view,name='update-user'),
    path('active-user/<userid>/<int:pk>', views.active_user_view,name='active-user'),
    path('admin-user-reset-password/<int:pk>', views.admin_user_reset_password_view,name='admin-user-reset-password'),
    path('inactive-user/<int:pk>', views.inactive_user_view,name='inactive-user'),
    path('delete-user/<userid>/<int:pk>', views.delete_user_view,name='delete-user'),

    # path('userlogin', LoginView.as_view(template_name='lxpapp/users/login.html'),name='userlogin'),
    path('register', LoginView.as_view(template_name='lxpapp/users/register.html'),name='register'),
    path('user-change-password', views.user_change_password_view,name='user-change-password'),
    path('termsandconditions', TemplateView.as_view(template_name='lxpapp/users/term-condition.html'),name='termsandconditions'),
    path('privacypolicy', TemplateView.as_view(template_name='lxpapp/users/privacy-policy.html'),name='privacypolicy'),
    path('ushms', TemplateView.as_view(template_name='blogs/ushms.html'),name='ushms'),

]
if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)