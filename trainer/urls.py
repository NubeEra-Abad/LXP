from django.urls import path
from trainer.trainerApiViews import *
urlpatterns = [
    path('scheduler-status/', SchedulerStatus.as_view(), name='api-scheduler-status'),
    path('scheduler-status-mark-done/', SchedulerStatusMarkDone.as_view(), name='api-scheduler-status-mark-done'),
    path('scheduler-status-sum/', SchedulerStatusSum.as_view(), name='api-scheduler-status-sum'),
    path('trainer-scheduler-calendar/', TrainerSchedulerCalendar.as_view(), name='api-trainer-scheduler-calendar'),
    path('activity-learner-list/', ActivityLearnerList.as_view(), name='api-activity-learner-list'),
    path('learner-batch-list/<int:learner_id>/', ActivityLearnerBatchList.as_view(), name='api-learner-batch-list'),
    path('activity-learner-batch/<int:activity_id>/', ActivityLearnerBatchActivity.as_view(), name='api-activity-learner-batch-activity'),
    path('activity-learner-batch-update-activity/', ActivityLearnerBatchActivityUpdate.as_view(), name='api-activity-learner-batch-update-activity'),
]