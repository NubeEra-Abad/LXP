from django.urls import path
from cfo import views
from django.contrib.auth.views import LoginView

urlpatterns = [

path('cfoclick', views.cfoclick_view),
path('cfologin', LoginView.as_view(template_name='cfo/cfologin.html'),name='cfologin'),
path('cfo-dashboard', views.cfo_dashboard_view,name='cfo-dashboard'),
path('cfo-manage-learner', views.cfo_manage_learner_view,name='cfo-manage-learner'),
path('cfo-active-learner/<userid>/<int:pk>', views.cfo_active_learner_view,name='cfo-active-learner'),
path('cfo-inactive-learner/<int:pk>', views.cfo_inactive_learner_view,name='cfo-inactive-learner'),
path('cfo-update-learner-course/<int:pk>', views.cfo_update_learner_course_view,name='cfo-update-learner-course'),

path('cfo-coursetype', views.cfo_coursetype_view,name='cfo-coursetype'),
path('cfo-add-coursetype', views.cfo_add_coursetype_view,name='cfo-add-coursetype'),
path('cfo-update-coursetype/<int:pk>', views.cfo_update_coursetype_view,name='cfo-update-coursetype'),
path('cfo-view-coursetype', views.cfo_view_coursetype_view,name='cfo-view-coursetype'),
path('cfo-delete-coursetype/<int:pk>', views.cfo_delete_coursetype_view,name='cfo-delete-coursetype'),

path('cfo-batch', views.cfo_batch_view,name='cfo-batch'),
path('cfo-add-batch', views.cfo_add_batch_view,name='cfo-add-batch'),
path('cfo-update-batch/<int:pk>', views.cfo_update_batch_view,name='cfo-update-batch'),
path('cfo-view-batch', views.cfo_view_batch_view,name='cfo-view-batch'),
path('cfo-delete-batch/<int:pk>', views.cfo_delete_batch_view,name='cfo-delete-batch'),
path('cfo-view-batch-details/<batchname>/<int:pk>', views.cfo_view_batch_details_view,name='cfo-view-batch-details'),

path('cfo-learnerfee', views.cfo_learnerfee_view,name='cfo-learnerfee'),
path('cfo-add-learnerfee', views.cfo_add_learnerfee_view,name='cfo-add-learnerfee'),
path('cfo-update-learnerfee/<int:pk>', views.cfo_update_learnerfee_view,name='cfo-update-learnerfee'),
path('cfo-view-learnerfee', views.cfo_view_learnerfee_view,name='cfo-view-learnerfee'),
path('cfo-delete-learnerfee/<int:pk>', views.cfo_delete_learnerfee_view,name='cfo-delete-learnerfee'),

]
