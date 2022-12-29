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
    
    path('trainer-pending-short-exam-reuslt', views.trainer_pending_short_exam_result_view,name='trainer-pending-short-exam-reuslt'),
    path('trainer-update-short-question-result/<int:pk>', views.trainer_update_short_question_result_view,name='trainer-update-short-question-result'),
    path('trainer-save-short-question-result/<int:pk>', views.trainer_save_short_question_result_view,name='trainer-save-short-question-result'),

    path('trainer-sync-youtube', views.trainer_sync_youtube_view,name='trainer-sync-youtube'),
    path('trainer-sync-youtube-start', views.trainer_sync_youtube_start_view,name='trainer-sync-youtube-start'),
    path('trainer-sync-youtube-byselected-playlist-start', views.trainer_sync_youtube_byselected_playlist_start_view,name='trainer-sync-youtube-byselected-playlist-start'),

    path('trainer-sync-video-folder', views.trainer_sync_video_folder_view,name='trainer-sync-video-folder'),
    path('trainer-start-sync-video-folder', views.trainer_start_sync_video_folder_view,name='trainer-start-sync-video-folder'),

    path('trainer-view-learner-video', views.trainer_view_learner_video_view,name='trainer-view-learner-video'),
    path('trainer-learner-video-course/<int:user_id>/<userfirstname>/<userlastname>', views.trainer_learner_video_Course_view,name='trainer-learner-video-course'),
    path('trainer-learner-video-course-subject/<int:course_id>', views.trainer_learner_video_Course_subject_view,name='trainer-learner-video-course-subject'),
    path('trainer-learner-video-list/<int:subject_id>,/<int:course_id>', views.trainer_learner_video_list_view,name='trainer-learner-video-list'),
    path('trainer-learner-show-video/<int:subject_id>,/<int:course_id>,/<int:video_id>', views.trainer_learner_show_video_view,name='trainer-learner-show-video'),

    path('trainer-material', views.trainer_material_view,name='trainer-material'),
    path('trainer-add-material', views.trainer_add_material_view,name='trainer-add-material'),
    path('trainer-update-material/<int:pk>', views.trainer_update_material_view,name='trainer-update-material'),
    path('trainer-view-material', views.trainer_view_material_view,name='trainer-view-material'),
    path('trainer-delete-material/<int:pk>', views.trainer_delete_material_view,name='trainer-delete-material'),
    path('trainer-show-material/<subjectname>,/<chaptername>,/<materialtype>,/<int:pk>', views.trainer_show_material_view,name='trainer-show-material'),
    path('trainer-view-material-chapters', views.trainer_material_chapters_view,name='trainer-view-material-chapters'),

    path('trainer-upload-file', views.trainer_upload_file_view,name='trainer-upload-file'),
    path('trainer-start-upload-file', views.trainer_start_upload_file_view,name='trainer-start-upload-file'),
]
