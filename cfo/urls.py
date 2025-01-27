from django.urls import path
from cfo.cfoApiViews import *
urlpatterns = [
    path('batch/', BatchAPIView.as_view(), name='batch-list-create'),
    path('batch/<int:pk>/', BatchAPIView.as_view(), name='batch-detail-update-delete'),
]