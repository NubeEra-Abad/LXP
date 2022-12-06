from django import forms
from django.contrib.auth.models import User
from . import models
from django import forms
from .models import (
    Course,CourseDetails,Subject,Chapter, Topic
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
from django.forms import ModelForm, inlineformset_factory
from django.forms import formset_factory
class CourseForm(ModelForm):
    class Meta:
        model = Course
        exclude = ()

class CourseDetailsForm(ModelForm):
    class Meta:
        model = CourseDetails
        exclude = ()

CourseDetailsFormset = inlineformset_factory(Course, CourseDetails,
                                            form=CourseDetailsForm, extra=2)

class UserCourseForm(forms.ModelForm):
    courseid=forms.ModelChoiceField(queryset=models.Course.objects.all(),empty_label="Course Name", to_field_name="id")
    class Meta:
        model=models.UserCourse
        fields=['remarks']
class CourseTypeForm(forms.ModelForm):
    class Meta:
        model=models.CourseType
        fields=['coursetype_name']
 
class BatchForm(forms.ModelForm):
    coursetypeID=forms.ModelChoiceField(queryset=models.CourseType.objects.all(),empty_label="Course Type Name", to_field_name="id")
    courseID=forms.ModelChoiceField(queryset=models.Course.objects.all(),empty_label="Course Name", to_field_name="id")
    class Meta:
        model=models.Batch
        fields=['batch_name','stdate','enddate']
        widgets = {
            'stdate': forms.DateInput(format='%d/%m/%Y'),
            'enddate': forms.DateInput(format='%d/%m/%Y')
        }
