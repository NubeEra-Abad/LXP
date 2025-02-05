from django.db.models import Sum, F, Value, Q, Count, F, Case, When, IntegerField
from rest_framework import serializers
from lxpapiapp.models import *
from datetime import datetime

class MaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Material
        fields = '__all__'

class SessionMaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = SessionMaterial
        fields = '__all__'
        
class McqQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = McqQuestion
        fields = '__all__'
        
class McqResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = McqResult
        fields = '__all__'

class McqResultDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = McqResultDetails
        fields = '__all__'

class ExamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exam
        fields = '__all__'

class ExamQuestionDettailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExamQuestionDettails
        fields = '__all__'

class ShortResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShortResult
        fields = '__all__'

class ShortResultDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShortResultDetails
        fields = '__all__'
        
class ShortQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShortQuestion
        fields = '__all__'

class PendingShortExamResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShortResult
        fields = ['id', 'learner', 'exam', 'marks', 'status', 'datecreate', 'timetaken']

class ShortResultDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShortResultDetails
        fields = ['id', 'shortresult', 'question', 'marks', 'answer', 'feedback']

class ShortResultDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShortResultDetails
        fields = ['id', 'marks', 'feedback', 'question', 'answer', 'shortresult']
        

class LearnerChapterSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField(max_length=255)
    watched = serializers.IntegerField()
    unlocked = serializers.IntegerField()

class LearnerSubjectSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField(max_length=255)
    vt_total = serializers.IntegerField()
    m_total = serializers.IntegerField()
    v_watched = serializers.IntegerField()
    per = serializers.FloatField()
    thumbnail_url = serializers.CharField(max_length=255)
    

class ChapterQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChapterQuestion
        fields = ['id', 'subject', 'chapter', 'question', 'option1', 'option2', 'option3', 'option4', 'answer', 'marks']

class ChapterResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChapterResult
        fields = ['id', 'learner', 'course', 'subject', 'chapter', 'marks', 'wrong', 'correct', 'timetaken', 'date']

class ChapterResultDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChapterResultDetails
        fields = ['id', 'chapterresult', 'question', 'selected']

class ActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Activity
        fields = '__all__'

class K8STerminalSerializer(serializers.ModelSerializer):
    class Meta:
        model = K8STerminal
        fields = ['id', 'trainer', 'learner', 'Password', 'usagevalue']