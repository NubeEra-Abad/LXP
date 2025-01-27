from django.urls import path
from cfo.cfoApiViews import *
urlpatterns = [
    path('batch/', BatchAPIView.as_view(), name='api-batch'),
    path('batch/<int:pk>/', BatchAPIView.as_view(), name='api-batch-detail'),
    
    path('schedulers/', SchedulerAPIView.as_view(), name='api-schedulers'),
    path('schedulers/<int:pk>/', SchedulerAPIView.as_view(), name='api-scheduler-detail'),
]