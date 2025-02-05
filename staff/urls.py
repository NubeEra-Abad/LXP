from django.urls import path
from staff.staffApiViews import *
urlpatterns = [
    path('material/', MaterialAPIView.as_view(), name='api-material'),
    path('material-upload-csv/', MaterialUploadDetailsCSVView.as_view(), name='api-material-upload-csv'),
    path('session-material/', SessionMaterialAPIView.as_view(), name='api-session-material'),
    path('mcq-questions/', McqQuestionAPIView.as_view(), name='api-mcq-question'),
    path('mcq-results/', McqResultAPIView.as_view(), name='api-mcq-result'),
    path('mcq-result-details/', McqResultDetailsAPIView.as_view(), name='api-mcq-result-details'),
    path('exams/', ExamAPIView.as_view(), name='api-exam'),
    path('exam-questions/', ExamQuestionDetailsAPIView.as_view(), name='api-exam-question'),
    path('short-results/', ShortResultAPIView.as_view(), name='api-short-results'),
    path('short-result-details/', ShortResultDetailsAPIView.as_view(), name='api-short-result-details'),
    path('short-questions/', ShortQuestionAPIView.as_view(), name='api-short-questions'),
    path('pending-short-exam-results/', PendingShortExamResultAPIView.as_view(), name='api-pending-short-exam-results'),
    path('update-short-question-result/<int:pk>/', UpdateShortQuestionResultAPIView.as_view(), name='api-update-short-question-result'),
    path('save-short-question-result/<int:pk>/', SaveShortQuestionResultAPIView.as_view(), name='api-save-short-question-result'),
    ############Those API is confusing due to many tables are removed so till dont use it #######################
    path('learner-chapter/', LearnerChapterView.as_view(), name='api-learner-chapter'),
    path('learner-chapter-course/<int:user_id>/', LearnerChapterCourseView.as_view(), name='api-learner-chapter-course'),
    path('learner-chapter-course-subject/<int:user_id>/', LearnerChapterCourseSubjectView.as_view(), name='api-learner-chapter-course-subject'),
    path('learner-chapter-list/<int:subject_id>/<int:user_id>/', LearnerChapterListView.as_view(), name='api-learner-chapter-list'),
    path('learner-approve-chapter/<int:pk>/<int:studid>/', LearnerApproveChapterView.as_view(), name='api-learner-approve-chapter'),
    path('learner-approve-all-chapter/<int:userid>/<int:subject_id>/', LearnerApproveAllChapterView.as_view(), name='api-learner-approve-all-chapter'),
    path('learner-show-chapter/<int:subject_id>/<int:chapter_id>/', LearnerShowChapterView.as_view(), name='api-learner-show-chapter'),
    ###################################
    path('chapter-questions/', ChapterQuestionListCreate.as_view(), name='api-chapter-question'),
    path('chapter-results/', ChapterResultListCreate.as_view(), name='api-chapter-result'),
    path('chapter-result-details/', ChapterResultDetailsListCreate.as_view(), name='api-chapter-result-details'),
    path('activity/', ActivityAPIView.as_view(), name='api-activity'),
    path('activity-upload-csv/', ActivityUploadDetailsCSVView.as_view(), name='api-activity-upload-csv'),
]