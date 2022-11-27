from django import forms
from django.contrib.auth.models import User
from . import models
from django import forms
from .models import (
    Course
)
from django.forms import inlineformset_factory
class ContactusForm(forms.Form):
    Name = forms.CharField(max_length=30)
    Email = forms.EmailField()
    Message = forms.CharField(max_length=500,widget=forms.Textarea(attrs={'rows': 3, 'cols': 30}))

class SubjectForm(forms.ModelForm):
    class Meta:
        model=models.Subject
        fields=['subject_name']

class ChapterForm(forms.ModelForm):
    subjectID=forms.ModelChoiceField(queryset=models.Subject.objects.all(),empty_label="Subject Name", to_field_name="id")
    class Meta:
        model=models.Chapter
        fields=['chapter_name']

class TopicForm(forms.ModelForm):
    subjectID=forms.ModelChoiceField(queryset=models.Subject.objects.all(),empty_label="Subject Name", to_field_name="id")
    chapterID=forms.ModelChoiceField(queryset=models.Chapter.objects.all(),empty_label="Chapter Name", to_field_name="id")
    class Meta:
        model=models.Topic
        fields=['topic_name']

from django.forms import formset_factory
class CourseForm(forms.ModelForm):
    class Meta:
        model=Course
        fields=['course_name']
CourseDetailsFormset = formset_factory(CourseForm, extra=1)
#VariantFormSet = inlineformset_factory(Course, Course, form= CourseForm,extra=1, can_delete=True,can_delete_extra=True)
        
class UserCourseForm(forms.ModelForm):
    courseid=forms.ModelChoiceField(queryset=models.Course.objects.all(),empty_label="Course Name", to_field_name="id")
    class Meta:
        model=models.UserCourse
        fields=['remarks']
    