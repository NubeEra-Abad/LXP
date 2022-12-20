from django import forms
from django.contrib.auth.models import User
from . import models
from django import forms
from .models import (
    Course,CourseDetails
)
from django.forms import ModelForm, inlineformset_factory
class ContactusForm(forms.Form):
    Name = forms.CharField(max_length=30)
    Email = forms.EmailField()
    Message = forms.CharField(max_length=500,widget=forms.Textarea(attrs={'rows': 3, 'cols': 30}))

class SubjectForm(forms.ModelForm):
    class Meta:
        model=models.Playlist
        fields=['name']

class ChapterForm(forms.ModelForm):
    subjectID=forms.ModelChoiceField(queryset=models.Playlist.objects.all() ,empty_label="Subject Name", to_field_name="id")
    class Meta:
        model=models.Video
        fields=['name']

class TopicForm(forms.ModelForm):
    subjectID=forms.ModelChoiceField(queryset=models.Playlist.objects.all().order_by('name'),empty_label="Subject Name", to_field_name="id")
    chapterID=forms.ModelChoiceField(queryset=models.Video.objects.all(),empty_label="Chapter Name", to_field_name="id")
    class Meta:
        model=models.Topic
        fields=['topic_name']

class CourseForm(ModelForm):
    class Meta:
        model = Course
        exclude = ()

class CourseDetailsForm(ModelForm):
    subjectID=forms.ModelChoiceField(queryset=models.Playlist.objects.all().order_by('name'),empty_label="Subject Name", to_field_name="id")
    chapterID=forms.ModelChoiceField(queryset=models.Video.objects.all().order_by('name'),empty_label="Chapter Name", to_field_name="id")
    topicID=forms.ModelChoiceField(queryset=models.Topic.objects.all().order_by('topic_name'),empty_label="Topic Name", to_field_name="id")
    class Meta:
        model = CourseDetails
        fields=['subject']
        fields=['chapter']
        fields=['topic']
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

class PassionateSkillForm(forms.ModelForm):
    class Meta:
        model=models.PassionateSkill
        fields=['passionateskill_name']

class KnownSkillForm(forms.ModelForm):
    class Meta:
        model=models.KnownSkill
        fields=['knownskill_name']

class LearnerDetailsForm(forms.ModelForm):
    class Meta:
        model=models.LearnerDetails
        fields=['user_full_name','mobile','iswhatsapp','whatsappno']

# class ExamForm(forms.ModelForm):
#     courseID=forms.ModelChoiceField(queryset=models.Course.objects.all(),empty_label="Course Name", to_field_name="id")
#     class Meta:
#         model=models.Exam
#         fields=['exam_name','questiontpye']

class ExamForm(forms.ModelForm):
    courseID=forms.ModelChoiceField(queryset=models.Course.objects.all() ,empty_label="Course Name", to_field_name="id")
    class Meta:
        model=models.Exam
        fields=['exam_name','questiontpye']

class McqQuestionForm(forms.ModelForm):
    examID=forms.ModelChoiceField(queryset=models.Exam.objects.all().filter(questiontpye='MCQ'),empty_label="Exam Name", to_field_name="id")
    class Meta:
        model=models.McqQuestion
        fields=['marks','question','option1','option2','option3','option4','answer']
        widgets = {
            'question': forms.Textarea(attrs={'rows': 3, 'cols': 50})
        }

class ShortQuestionForm(forms.ModelForm):
    examID=forms.ModelChoiceField(queryset=models.Exam.objects.all().filter(questiontpye='ShortAnswer'),empty_label="Exam Name", to_field_name="id")
    class Meta:
        model=models.McqQuestion
        fields=['marks','question']
        widgets = {
            'question': forms.Textarea(attrs={'rows': 3, 'cols': 50})
        }

class PlayListForm(forms.ModelForm):
    class Meta:
        model=models.Playlist
        fields=['name','playlist_id']
