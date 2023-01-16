from django.urls import path
from learner import views
from django.contrib.auth.views import LoginView
from learner.views import CreateCrudUser, CrudView, DeleteCrudUser, UpdateCrudUser
urlpatterns = [
path('learnerclick', views.learnerclick_view),
path('learnerlogin', LoginView.as_view(template_name='learner/learnerlogin.html'),name='learnerlogin'),
path('learner-dashboard', views.learner_dashboard_view,name='learner-dashboard'),
path('learner-exam', views.learner_exam_view,name='learner-exam'),
path('learner-take-exam/<int:pk>', views.learner_take_exam_view,name='learner-take-exam'),
path('learner-start-exam/<int:pk>', views.learner_start_exam_view,name='learner-start-exam'),
path('learner-show-exam-reuslt/<int:pk>', views.learner_show_exam_reuslt_view,name='learner-show-exam-reuslt'),
path('learner-show-exam-reuslt-details/<int:pk>', views.learner_show_exam_reuslt_details_view,name='learner-show-exam-reuslt-details'),

path('learner-short-exam', views.learner_short_exam_view,name='learner-short-exam'),
path('learner-take-short-exam/<int:pk>', views.learner_take_short_exam_view,name='learner-take-short-exam'),
path('learner-start-short-exam/<int:pk>', views.learner_start_short_exam_view,name='learner-start-short-exam'),
path('learner-show-short-exam-reuslt/<int:pk>', views.learner_show_short_exam_reuslt_view,name='learner-show-short-exam-reuslt'),
path('learner-show-short-exam-reuslt-details/<int:pk>', views.learner_show_short_exam_reuslt_details_view,name='learner-show-short-exam-reuslt-details'),

path('learner-video-course', views.learner_video_Course_view,name='learner-video-course'),
path('learner-video-course-subject/<int:course_id>', views.learner_video_Course_subject_view,name='learner-video-course-subject'),
path('learner-video-list/<int:subject_id>,/<int:course_id>', views.learner_video_list_view,name='learner-video-list'),
path('learner-show-video/<int:subject_id>,/<int:course_id>,/<int:video_id>', views.learner_show_video_view,name='learner-show-video'),
path('learner-see-material/<subject_id>/<chapter_id>/<course_id>/<int:pk>', views.learner_see_material_view,name='learner-see-material'),

path('learner-check-k8sterminal', views.learner_check_k8sterminal_view,name='learner-check-k8sterminal'),

# Django Ajax CRUD Operations
    path('crud/', CrudView.as_view(), name='crud_ajax'),
    path('ajax/crud/create/', CreateCrudUser.as_view(), name='crud_ajax_create'),
    path('ajax/crud/delete/', DeleteCrudUser.as_view(), name='crud_ajax_delete'),
    path('ajax/crud/update/', UpdateCrudUser.as_view(), name='crud_ajax_update'),

    path('learner-pyton-terminal', views.learner_python_terminal_view,name='learner-pyton-terminal'),
    path('learner-linux-terminal', views.learner_linux_terminal_view,name='learner-linux-terminal'),
]
