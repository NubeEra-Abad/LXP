from django.db.models import Sum, F, Value, Q, Count, F, Case, When, IntegerField
from rest_framework import serializers
from lxpapiapp.models import *
from datetime import datetime

class CourseTypeSerializer(serializers.ModelSerializer):
    """
    Serializer for CourseType model.
    
    Fields:
    - id: Auto-generated primary key.
    - coursetype_name: Name of the course type.
    """
    class Meta:
        model = CourseType
        fields = ['id', 'coursetype_name']

class BatchCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = BatchCourse
        fields = ['id', 'batch', 'course_name']


class BatchTrainerSerializer(serializers.ModelSerializer):
    class Meta:
        model = BatchTrainer
        fields = ['id', 'batch', 'trainer_name']


class BatchLearnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = BatchLearner
        fields = ['id', 'batch', 'learner_name', 'fee']  # Include fee field


class BatchRecordedVDOListSerializer(serializers.ModelSerializer):
    class Meta:
        model = BatchRecordedVDOList
        fields = ['id', 'batch', 'video_title']


class BatchSerializer(serializers.ModelSerializer):
    courses = BatchCourseSerializer(many=True, read_only=True)
    trainers = BatchTrainerSerializer(many=True, read_only=True)
    learners = BatchLearnerSerializer(many=True, read_only=True)
    videos = BatchRecordedVDOListSerializer(many=True, read_only=True)

    class Meta:
        model = Batch
        fields = ['id', 'batch_name', 'coursetype', 'stdate', 'enddate', 'courses', 'trainers', 'learners', 'videos']
        
class SchedulerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Scheduler
        fields = '__all__'