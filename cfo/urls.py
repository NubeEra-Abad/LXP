from django.urls import path
from cfo import views
from django.contrib.auth.views import LoginView

urlpatterns = [

path('cfoclick', views.cfoclick_view),
path('cfologin', LoginView.as_view(template_name='cfo/cfologin.html'),name='cfologin'),
path('cfo-dashboard', views.cfo_dashboard_view,name='cfo-dashboard'),
path('cfo-manage-learner', views.cfo_manage_learner_view,name='cfo-manage-learner'),
path('cfo-active-learner/<int:pk>', views.cfo_active_learner_view,name='cfo-active-learner'),
path('cfo-inactive-learner/<int:pk>', views.cfo_inactive_learner_view,name='cfo-inactive-learner'),
path('cfo-update-learner-course/<int:pk>', views.cfo_update_learner_course_view,name='cfo-update-learner-course'),


]
