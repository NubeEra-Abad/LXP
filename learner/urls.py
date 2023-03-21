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

    path('learner-video-course', views.learner_video_Course_view,name='learner-video-course'),
    path('learner-video-course-subject', views.learner_video_Course_subject_view,name='learner-video-course-subject'),
    path('learner-video-list/<int:subject_id>', views.learner_video_list_view,name='learner-video-list'),
    path('learner-show-video/<int:subject_id>,/<int:video_id>', views.learner_show_video_view,name='learner-show-video'),
    path('learner-video-sesseionmaterial-list/<subject_id>/<video_id>', views.learner_video_sesseionmaterial_list_view,name='learner-video-sesseionmaterial-list'),
    path('learner-see-sesseionmaterial/<subject_id>/<video_id>/<int:pk>', views.learner_see_sesseionmaterial_view,name='learner-see-sesseionmaterial'),

    path('learner-studymaterial-course', views.learner_studymaterial_course_view,name='learner-studymaterial-course'),
    path('learner-studymaterial-course-subject/<coursename>/<int:courseset_id>', views.learner_studymaterial_course_subject_view,name='learner-studymaterial-course-subject'),
    path('learner-studymaterial-subject-chapter/<coursename>/<subjectname>/<int:subject_id>/<int:courseset_id>', views.learner_studymaterial_subject_chapter_view,name='learner-studymaterial-subject-chapter'),
    path('learner-studymaterial-chapter-topic/<coursename>/<subjectname>/<chaptername>/<int:subject_id>/<int:chapter_id>/<int:courseset_id>', views.learner_studymaterial_chapter_topic_view,name='learner-studymaterial-chapter-topic'),
]
