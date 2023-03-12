from django.urls import path
from trainer import views
from django.contrib.auth.views import LoginView

urlpatterns = [

    path('trainer-dashboard', views.trainer_dashboard_view,name='trainer-dashboard'),
    path('trainer-material', views.trainer_material_view,name='trainer-material'),
    path('trainer-add-material', views.trainer_add_material_view,name='trainer-add-material'),
    path('trainer-update-material/<int:pk>', views.trainer_update_material_view,name='trainer-update-material'),
    path('trainer-view-material', views.trainer_view_material_view,name='trainer-view-material'),
    path('trainer-delete-material/<int:pk>', views.trainer_delete_material_view,name='trainer-delete-material'),
    path('trainer-show-material/<materialtype>,/<int:pk>', views.trainer_show_material_view,name='trainer-show-material'),
    path('trainer-material-upload-file', views.trainer_material_upload_file_view,name='trainer-material-upload-file'),
    path('trainer-material-start-upload-file', views.trainer_material_start_upload_file_view,name='trainer-material-start-upload-file'),
    path('trainer-upload-material-details-csv', views.trainer_upload_material_details_csv_view,name='trainer-upload-material-details-csv'),

    path('trainer-exam', views.trainer_exam_view,name='trainer-exam'),
    path('trainer-add-exam', views.trainer_add_exam_view,name='trainer-add-exam'),
    path('trainer-update-exam/<int:pk>', views.trainer_update_exam_view,name='trainer-update-exam'),
    path('trainer-view-exam', views.trainer_view_exam_view,name='trainer-view-exam'),
    path('trainer-view-filter-exam/<type>', views.trainer_view_filter_exam_view,name='trainer-view-filter-exam'),
    path('trainer-delete-exam/<int:pk>', views.trainer_delete_exam_view,name='trainer-delete-exam'),
    path('trainer-upload-exam-csv', views.trainer_upload_exam_csv_view,name='trainer-upload-exam-csv'),
     
    path('trainer-mcqquestion', views.trainer_mcqquestion_view,name='trainer-mcqquestion'),
    path('trainer-add-mcqquestion', views.trainer_add_mcqquestion_view,name='trainer-add-mcqquestion'),
    path('trainer-update-mcqquestion/<int:pk>', views.trainer_update_mcqquestion_view,name='trainer-update-mcqquestion'),
    path('trainer-view-mcqquestion-exams', views.trainer_view_mcqquestion_exams_view,name='trainer-view-mcqquestion-exams'),
    path('trainer-view-mcqquestion/<int:examid>', views.trainer_view_mcqquestion_view,name='trainer-view-mcqquestion'),
    path('trainer-delete-mcqquestion/<int:pk>', views.trainer_delete_mcqquestion_view,name='trainer-delete-mcqquestion'),

    path('trainer-shortquestion', views.trainer_shortquestion_view,name='trainer-shortquestion'),
    path('trainer-add-shortquestion', views.trainer_add_shortquestion_view,name='trainer-add-shortquestion'),
    path('trainer-update-shortquestion/<int:pk>', views.trainer_update_shortquestion_view,name='trainer-update-shortquestion'),
    path('trainer-view-shortquestion', views.trainer_view_shortquestion_view,name='trainer-view-shortquestion'),
    path('trainer-delete-shortquestion/<int:pk>', views.trainer_delete_shortquestion_view,name='trainer-delete-shortquestion'),
    
    path('trainer-pending-short-exam-reuslt', views.trainer_pending_short_exam_result_view,name='trainer-pending-short-exam-reuslt'),
    path('trainer-update-short-question-result/<int:pk>', views.trainer_update_short_question_result_view,name='trainer-update-short-question-result'),
    path('trainer-save-short-question-result/<int:pk>', views.trainer_save_short_question_result_view,name='trainer-save-short-question-result'),

    path('trainer-ytexamquestion', views.trainer_ytexamquestion_view,name='trainer-ytexamquestion'),
    path('trainer-add-ytexamquestion', views.trainer_add_ytexamquestion_view,name='trainer-add-ytexamquestion'),
    path('trainer-update-ytexamquestion/<int:pk>', views.trainer_update_ytexamquestion_view,name='trainer-update-ytexamquestion'),
    path('trainer-view-ytexamquestion', views.trainer_view_ytexamquestion_view,name='trainer-view-ytexamquestion'),
    path('trainer-delete-ytexamquestion/<int:pk>', views.trainer_delete_ytexamquestion_view,name='trainer-delete-ytexamquestion'),
]
