from django.db.models import Sum, F, Value, Q, Count, F, Case, When, IntegerField
from rest_framework import serializers
from lxpapiapp.models import *
from datetime import datetime
class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ['id', 'subject_name']
        
class ChapterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chapter
        fields = ['id', 'chapter_name', 'subject']
        
class TopicSerializer(serializers.ModelSerializer):
    subject = serializers.SerializerMethodField()

    class Meta:
        model = Topic
        fields = ['id', 'topic_name', 'chapter', 'subject']

    def get_subject(self, obj):
        if obj.chapter:
            return obj.chapter.subject.id if obj.chapter.subject else None
        return None

class MainHeadSerializer(serializers.ModelSerializer):
    class Meta:
        model = MainHead
        fields = ['id', 'mainhead_name']

class SubHeadSerializer(serializers.ModelSerializer):
    mainhead_name = serializers.ReadOnlyField(source='mainhead.mainhead_name')

    class Meta:
        model = SubHead
        fields = ['id', 'mainhead', 'mainhead_name', 'subhead_name']

class CourseChapterSerializer(serializers.ModelSerializer):
    subject_name = serializers.CharField(source='subject.subject_name', read_only=True)
    chapter_name = serializers.CharField(source='chapter.chapter_name', read_only=True)

    class Meta:
        model = CourseChapter
        fields = ['id', 'course', 'subject', 'subject_name', 'chapter', 'chapter_name']

class CourseSerializer(serializers.ModelSerializer):
    chapters = CourseChapterSerializer(many=True, read_only=True)

    class Meta:
        model = Course
        fields = [
            'id', 'course_name', 'description', 'whatlearn', 'includes',
            'themecolor', 'tags', 'image', 'banner', 'price', 'mainhead', 'subhead', 'chapters'
        ]

class CourseCreateUpdateSerializer(serializers.ModelSerializer):
    chapters = serializers.ListField(
        child=serializers.DictField(),
        write_only=True,
        required=False
    )

    class Meta:
        model = Course
        fields = [
            'id', 'course_name', 'description', 'whatlearn', 'includes',
            'themecolor', 'tags', 'image', 'banner', 'price', 'mainhead', 'subhead', 'chapters'
        ]

    def create(self, validated_data):
        chapters_data = validated_data.pop('chapters', [])
        course = Course.objects.create(**validated_data)
        for chapter_data in chapters_data:
            subject = Subject.objects.get(id=chapter_data['subject'])
            chapter = Chapter.objects.get(id=chapter_data['chapter'])
            CourseChapter.objects.create(course=course, subject=subject, chapter=chapter)
        return course

    def update(self, instance, validated_data):
        chapters_data = validated_data.pop('chapters', [])
        instance = super().update(instance, validated_data)

        if chapters_data:
            instance.chapters.all().delete()  # Clear existing chapters
            for chapter_data in chapters_data:
                subject = Subject.objects.get(id=chapter_data['subject'])
                chapter = Chapter.objects.get(id=chapter_data['chapter'])
                CourseChapter.objects.create(course=instance, subject=subject, chapter=chapter)

        return instance
    
