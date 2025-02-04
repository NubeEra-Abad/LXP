from django.urls import path
from cto.ctoApiViews import *
urlpatterns = [
    path('subject/', SubjectAPIView.as_view(), name='api-subject'),
    path('chapter/', ChapterAPIView.as_view(), name='api-chapter-list'),
    path('chapter/<int:chapter_id>/', ChapterAPIView.as_view(), name='api-chapter-detail'),
    path('topic/', TopicAPIView.as_view(), name='api-topic-list'),
    path('topic/<int:topic_id>/', TopicAPIView.as_view(), name='api-topic-detail'),
    path('category/', CategoryAPIView.as_view(), name='api-category-list'),
    path('category/<int:category_id>/', CategoryAPIView.as_view(), name='api-category-detail'),
    path('subcategory/', SubCategoryAPIView.as_view(), name='api-subcategory-list'),
    path('subcategory/<int:subcategory_id>/', SubCategoryAPIView.as_view(), name='api-subcategory-detail'),
    path('courses/', CourseAPIView.as_view(), name='api-course-list'),
    path('courses/<int:pk>/', CourseAPIView.as_view(), name='api-course-detail'),
    path('courses/<int:pk>/course-chapters/', CourseChapterDetailView.as_view()),  # Retrieve chapters for a specific course
    path('course-chapters/', CourseChapterDetailView.as_view()),  # Retrieve all course chapters
    
    path('sync-youtube/', SyncYouTubeAPIView.as_view(), name='api-sync-youtube'),
    
]