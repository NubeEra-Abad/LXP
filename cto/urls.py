from django.urls import path
from cto import views
from django.contrib.auth.views import LoginView

urlpatterns = [

path('ctoclick', views.ctoclick_view),
path('ctologin', LoginView.as_view(template_name='cto/ctologin.html'),name='ctologin'),
path('cto-dashboard', views.cto_dashboard_view,name='cto-dashboard'),

path('cto-subject', views.cto_subject_view,name='cto-subject'),
path('cto-add-subject', views.cto_add_subject_view,name='cto-add-subject'),
path('cto-update-subject/<int:pk>', views.cto_update_subject_view,name='cto-update-subject'),
path('cto-view-subject', views.cto_view_subject_view,name='cto-view-subject'),
path('cto-delete-subject/<int:pk>', views.cto_delete_subject_view,name='cto-delete-subject'),

path('cto-chapter', views.cto_chapter_view,name='cto-chapter'),
path('cto-add-chapter', views.cto_add_chapter_view,name='cto-add-chapter'),
path('cto-update-chapter/<int:pk>', views.cto_update_chapter_view,name='cto-update-chapter'),
path('cto-view-chapter', views.cto_view_chapter_view,name='cto-view-chapter'),
path('cto-delete-chapter/<int:pk>', views.cto_delete_chapter_view,name='cto-delete-chapter'),

path('cto-topic', views.cto_topic_view,name='cto-topic'),
path('cto-add-topic', views.cto_add_topic_view,name='cto-add-topic'),
path('cto-update-topic/<int:pk>', views.cto_update_topic_view,name='cto-update-topic'),
path('cto-view-topic', views.cto_view_topic_view,name='cto-view-topic'),
path('cto-delete-topic/<int:pk>', views.cto_delete_topic_view,name='cto-delete-topic'),

path('cto-course', views.cto_course_view,name='cto-course'),
path('cto-add-course', views.cto_add_course_view,name='cto-add-course'),
path('cto-view-course', views.cto_view_course_view,name='cto-view-course'),
path('cto-delete-course/<int:pk>', views.cto_delete_course_view,name='cto-delete-course'),

]
