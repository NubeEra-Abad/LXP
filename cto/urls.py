from django.urls import path
from cto import views
from django.contrib.auth.views import LoginView
urlpatterns = [

    path('ctoclick', views.ctoclick_view),
    path('ctologin', LoginView.as_view(template_name='cto/ctologin.html'),name='ctologin'),
    path('cto-dashboard', views.cto_dashboard_view,name='cto-dashboard'),

    path('cto-passionateskill', views.cto_passionateskill_view,name='cto-passionateskill'),
    path('cto-add-passionateskill', views.cto_add_passionateskill_view,name='cto-add-passionateskill'),
    path('cto-update-passionateskill/<int:pk>', views.cto_update_passionateskill_view,name='cto-update-passionateskill'),
    path('cto-view-passionateskill', views.cto_view_passionateskill_view,name='cto-view-passionateskill'),
    path('cto-delete-passionateskill/<int:pk>', views.cto_delete_passionateskill_view,name='cto-delete-passionateskill'),

    path('cto-knownskill', views.cto_knownskill_view,name='cto-knownskill'),
    path('cto-add-knownskill', views.cto_add_knownskill_view,name='cto-add-knownskill'),
    path('cto-update-knownskill/<int:pk>', views.cto_update_knownskill_view,name='cto-update-knownskill'),
    path('cto-view-knownskill', views.cto_view_knownskill_view,name='cto-view-knownskill'),
    path('cto-delete-knownskill/<int:pk>', views.cto_delete_knownskill_view,name='cto-delete-knownskill'),

    path('cto-subject', views.cto_subject_view,name='cto-subject'),
    path('cto-add-subject', views.cto_add_subject_view,name='cto-add-subject'),
    path('cto-update-subject/<int:pk>', views.cto_update_subject_view,name='cto-update-subject'),
    path('cto-view-subject', views.cto_view_subject_view,name='cto-view-subject'),
    path('cto-delete-subject/<int:pk>', views.cto_delete_subject_view,name='cto-delete-subject'),
    path('cto-upload-subject-details-csv', views.cto_upload_subject_details_csv_view,name='cto-upload-subject-details-csv'),

    path('cto-module', views.cto_module_view,name='cto-module'),
    path('cto-add-module', views.cto_add_module_view,name='cto-add-module'),
    path('cto-update-module/<int:pk>', views.cto_update_module_view,name='cto-update-module'),
    path('cto-view-module', views.cto_view_module_view,name='cto-view-module'),
    path('cto-delete-module/<int:pk>', views.cto_delete_module_view,name='cto-delete-module'),

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
    path('cto-update-course/<coursename>/<int:pk>', views.cto_update_course_view,name='cto-update-course'),
    path('cto-view-course', views.cto_view_course_view,name='cto-view-course'),
    path('cto-view-course-details/<coursename>/<int:pk>', views.cto_view_course_details_view,name='cto-view-course-details'),
    path('cto-delete-course/<int:pk>', views.cto_delete_course_view,name='cto-delete-course'),
    path('cto-upload-course-details-csv', views.cto_upload_course_details_csv_view,name='cto-upload-course-details-csv'),

    path('cto-courseset', views.cto_courseset_view,name='cto-courseset'),
    path('cto-add-courseset', views.cto_add_courseset_view,name='cto-add-courseset'),
    path('cto-update-courseset/<coursesetname>/<int:pk>', views.cto_update_courseset_view,name='cto-update-courseset'),
    path('cto-view-courseset', views.cto_view_courseset_view,name='cto-view-courseset'),
    path('cto-view-courseset-details/<coursesetname>/<int:pk>', views.cto_view_courseset_details_view,name='cto-view-courseset-details'),
    path('cto-delete-courseset/<int:pk>', views.cto_delete_courseset_view,name='cto-delete-courseset'),
    path('cto-upload-courseset-details-csv', views.cto_upload_courseset_details_csv_view,name='cto-upload-courseset-details-csv'),

    path('course_changelist', views.CourseListView.as_view(), name='course_changelist'),
    path('add/', views.CourseCreateView.as_view(), name='course_add'),
    path('<int:pk>/', views.CourseUpdateView.as_view(), name='course_change'),
    path('ajax/load-modules/', views.load_modules, name='ajax_load_modules'),
    path('ajax/load-chapters/', views.load_chapters, name='ajax_load_chapters'),
    path('ajax/load-topics/', views.load_topics, name='ajax_load_topics'),

    path('cto-sync-youtube', views.cto_sync_youtube_view,name='cto-sync-youtube'),
    path('cto-include-playlist', views.cto_include_playlist_view,name='cto-include-playlist'),
    path('cto-include-playlist-save', views.cto_include_playlist_save_view,name='cto-include-playlist-save'),
    path('cto-sync-youtube-start', views.cto_sync_youtube_start_view,name='cto-sync-youtube-start'),
    path('cto-sync-youtube-byselected-playlist-start', views.cto_sync_youtube_byselected_playlist_start_view,name='cto-sync-youtube-byselected-playlist-start'),
    
    path('cto-trainernotification', views.cto_trainernotification_view,name='cto-trainernotification'),
    path('cto-add-trainernotification', views.cto_add_trainernotification_view,name='cto-add-trainernotification'),
    path('cto-update-trainernotification/<int:pk>', views.cto_update_trainernotification_view,name='cto-update-trainernotification'),
    path('cto-view-trainernotification', views.cto_view_trainernotification_view,name='cto-view-trainernotification'),
    path('cto-delete-trainernotification/<int:pk>', views.cto_delete_trainernotification_view,name='cto-delete-trainernotification'),

]
