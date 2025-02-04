from django.db.models import Sum, F, Value, Q, Count, F, Case, When, IntegerField
from rest_framework import serializers
from lxpapiapp.models import *
from datetime import datetime
class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ['id', 'subject_name']
        
class ChapterSerializer(serializers.ModelSerializer):
    subject = SubjectSerializer()
    class Meta:
        model = Chapter
        fields = ['id', 'chapter_name', 'subject']
        
class TopicSerializer(serializers.ModelSerializer):
    subject = SubjectSerializer()
    chapter = ChapterSerializer()

    class Meta:
        model = Topic
        fields = ['id', 'topic_name', 'chapter', 'subject']

    def get_subject(self, obj):
        if obj.chapter:
            return obj.chapter.subject.id if obj.chapter.subject else None
        return None

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'category_name']

class SubCategorySerializer(serializers.ModelSerializer):
    category_name = serializers.ReadOnlyField(source='category.category_name')

    class Meta:
        model = SubCategory
        fields = ['id', 'category', 'category_name', 'subcategory_name']

class CourseChapterSerializer(serializers.ModelSerializer):
    subject_name = serializers.CharField(source='subject.subject_name', read_only=True)
    chapter_name = serializers.CharField(source='chapter.chapter_name', read_only=True)

    class Meta:
        model = CourseChapter
        fields = ['id', 'course', 'subject', 'subject_name', 'chapter', 'chapter_name']

class CourseSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.category_name', read_only=True)
    subcategory_name = serializers.CharField(source='subcategory.subcategory_name', read_only=True)

    # Serialize the chapters related to the course
    chapters = CourseChapterSerializer(many=True, read_only=True)

    class Meta:
        model = Course
        fields = [
            'id', 'course_name', 'description', 'whatlearn', 'includes',
            'themecolor', 'tags', 'image', 'banner', 'price', 'category', 'subcategory',
            'category_name', 'subcategory_name', 'chapters'
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
            'themecolor', 'tags', 'image', 'banner', 'price', 'category', 'subcategory', 'chapters'
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
    
