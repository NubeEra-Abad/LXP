from django.urls import path
from learner import views
urlpatterns = [
path('learnerclick', views.learnerclick_view),
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

]
