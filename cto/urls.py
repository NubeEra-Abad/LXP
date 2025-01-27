from django.urls import path
from cto.ctoApiViews import *
urlpatterns = [
    path('subject/', SubjectAPIView.as_view(), name='api-subject'),
    path('chapter/', ChapterAPIView.as_view(), name='api-chapter-list'),
    path('chapter/<int:chapter_id>/', ChapterAPIView.as_view(), name='api-chapter-detail'),
    path('topic/', TopicAPIView.as_view(), name='api-topic-list'),
    path('topic/<int:topic_id>/', TopicAPIView.as_view(), name='api-topic-detail'),
    path('mainhead/', MainHeadAPIView.as_view(), name='api-mainhead-list'),
    path('mainhead/<int:mainhead_id>/', MainHeadAPIView.as_view(), name='api-mainhead-detail'),
    path('subhead/', SubHeadAPIView.as_view(), name='api-subhead-list'),
    path('subhead/<int:subhead_id>/', SubHeadAPIView.as_view(), name='api-subhead-detail'),
    path('courses/', CourseAPIView.as_view(), name='api-course-list'),
    path('courses/<int:pk>/', CourseAPIView.as_view(), name='api-course-detail'),
    
    path('sync-youtube/', SyncYouTubeAPIView.as_view(), name='api-sync-youtube'),
    
]