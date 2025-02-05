from django.db.models import Sum, F, Value, Q, Count, F, Case, When, IntegerField
from rest_framework import serializers
from lxpapiapp.models import *
from datetime import datetime

class SchedulerStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = SchedulerStatus
        fields = ['id', 'date', 'scheduler', 'trainer', 'status']

class TrainerSchedulerCalendarSerializer(serializers.ModelSerializer):
    status_sum = serializers.IntegerField()
    completion_date = serializers.DateField(allow_null=True)

    class Meta:
        model = Scheduler
        fields = ['id', 'name', 'trainer', 'status_sum', 'completion_date']
        