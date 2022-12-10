from django.urls import path
from trainer import views
from django.contrib.auth.views import LoginView

urlpatterns = [

    path('trainerclick', views.trainerclick_view),
    path('trainerlogin', LoginView.as_view(template_name='trainer/trainerlogin.html'),name='trainerlogin'),
    path('trainer-dashboard', views.trainer_dashboard_view,name='trainer-dashboard'),

    path('trainer-exam', views.trainer_exam_view,name='trainer-exam'),
    path('trainer-add-exam', views.trainer_add_exam_view,name='trainer-add-exam'),
    path('trainer-update-exam/<int:pk>', views.trainer_update_exam_view,name='trainer-update-exam'),
    path('trainer-view-exam', views.trainer_view_exam_view,name='trainer-view-exam'),
    path('trainer-delete-exam/<int:pk>', views.trainer_delete_exam_view,name='trainer-delete-exam'),
    
    path('trainer-mcqquestion', views.trainer_mcqquestion_view,name='trainer-mcqquestion'),
    path('trainer-add-mcqquestion', views.trainer_add_mcqquestion_view,name='trainer-add-mcqquestion'),
    path('trainer-update-mcqquestion/<int:pk>', views.trainer_update_mcqquestion_view,name='trainer-update-mcqquestion'),
    path('trainer-view-mcqquestion', views.trainer_view_mcqquestion_view,name='trainer-view-mcqquestion'),
    path('trainer-delete-mcqquestion/<int:pk>', views.trainer_delete_mcqquestion_view,name='trainer-delete-mcqquestion'),

    path('trainer-shortquestion', views.trainer_shortquestion_view,name='trainer-shortquestion'),
    path('trainer-add-shortquestion', views.trainer_add_shortquestion_view,name='trainer-add-shortquestion'),
    path('trainer-update-shortquestion/<int:pk>', views.trainer_update_shortquestion_view,name='trainer-update-shortquestion'),
    path('trainer-view-shortquestion', views.trainer_view_shortquestion_view,name='trainer-view-shortquestion'),
    path('trainer-delete-shortquestion/<int:pk>', views.trainer_delete_shortquestion_view,name='trainer-delete-shortquestion'),
]
