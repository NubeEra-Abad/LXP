from django import forms
from django.contrib.auth.models import User
from . import models
from django import forms
from .models import (
    Course,CourseDetails
)
from django.db.models import Q
from social_django.models import UserSocialAuth
from django.forms import ModelForm, inlineformset_factory,modelformset_factory

class ContactusForm(forms.Form):
    Name = forms.CharField(max_length=30)
    Email = forms.EmailField()
    Message = forms.CharField(max_length=500,widget=forms.Textarea(attrs={'rows': 3, 'cols': 30}))

class SubjectForm(forms.ModelForm):
    name = forms.CharField(
        max_length=255,
        #  forms ↓
        widget=forms.TextInput(attrs={'autofocus': True})
    )
    class Meta:
        model=models.Playlist
        fields=['name']

class ChapterForm(forms.ModelForm):
    subjectID=forms.ModelChoiceField(queryset=models.Playlist.objects.all() ,empty_label="Subject Name", to_field_name="id")
    name = forms.CharField(
        max_length=255,
        #  forms ↓
        widget=forms.TextInput(attrs={'autofocus': True})
    )
    class Meta:
        model=models.Video
        fields=['name']

class TopicForm(forms.ModelForm):
    subjectID=forms.ModelChoiceField(queryset=models.Playlist.objects.all().order_by('name'),empty_label="Subject Name", to_field_name="id")
    chapterID=forms.ModelChoiceField(queryset=models.Video.objects.all(),empty_label="Chapter Name", to_field_name="id")
    topic_name = forms.CharField(
        max_length=255,
        #  forms ↓
        widget=forms.TextInput(attrs={'autofocus': True})
    )
    class Meta:
        model=models.Topic
        fields=['topic_name']

class CourseForm(ModelForm):
    class Meta:
        model = Course
        fields=['course_name']
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
                                            form=CourseDetailsForm, extra=5)
CourseDetFormSet = modelformset_factory(
    CourseDetails, fields=("subject","chapter", "topic"), extra=1
)
class UserCourseForm(forms.ModelForm):
    courseid=forms.ModelChoiceField(queryset=models.Course.objects.all(),empty_label="Course Name", to_field_name="id")
    class Meta:
        model=models.UserCourse
        fields=['remarks']
class CourseTypeForm(forms.ModelForm):
    coursetype_name = forms.CharField(
        max_length=255,
        #  forms ↓
        widget=forms.TextInput(attrs={'autofocus': True})
    )
    class Meta:
        model=models.CourseType
        fields=['coursetype_name']
 
class BatchForm(forms.ModelForm):
    coursetypeID=forms.ModelChoiceField(queryset=models.CourseType.objects.all(),empty_label="Course Type Name", to_field_name="id")
    batch_name = forms.CharField(
        max_length=255,
        #  forms ↓
        widget=forms.TextInput(attrs={'autofocus': True})
    )
    class Meta:
        model=models.Batch
        fields=['batch_name','stdate','enddate']
        widgets = {
            'stdate': forms.DateInput(format='%d/%m/%Y'),
            'enddate': forms.DateInput(format='%d/%m/%Y')
        }

class LearnerFeeForm(forms.ModelForm):
    learnerID=forms.ModelChoiceField(queryset=models.User.objects.all(),empty_label="Learner Name", to_field_name="id")
    class Meta:
        model=models.LearnerFee
        fields=['fee','paiddate']
        widgets = {
            'paiddate': forms.DateInput(format='%d/%m/%Y')
        }


class PassionateSkillForm(forms.ModelForm):
    passionateskill_name = forms.CharField(
        max_length=255,
        #  forms ↓
        widget=forms.TextInput(attrs={'autofocus': True})
    )
    class Meta:
        model=models.PassionateSkill
        fields=['passionateskill_name']

class KnownSkillForm(forms.ModelForm):
    knownskill_name = forms.CharField(
        max_length=255,
        #  forms ↓
        widget=forms.TextInput(attrs={'autofocus': True})
    )
    class Meta:
        model=models.KnownSkill
        fields=['knownskill_name']

class LearnerDetailsForm(forms.ModelForm):
    user_full_name = forms.CharField(
        max_length=255,
        #  forms ↓
        widget=forms.TextInput(attrs={'autofocus': True})
    )
    class Meta:
        model=models.LearnerDetails
        fields=['user_full_name','mobile','iswhatsapp','whatsappno']

# class ExamForm(forms.ModelForm):
#     courseID=forms.ModelChoiceField(queryset=models.Course.objects.all(),empty_label="Course Name", to_field_name="id")
#     class Meta:
#         model=models.Exam
#         fields=['exam_name','questiontpye']

class ExamForm(forms.ModelForm):
    batchID=forms.ModelChoiceField(queryset=models.Batch.objects.all() ,empty_label="Batch Name", to_field_name="id")
    exam_name = forms.CharField(
        max_length=255,
        #  forms ↓
        widget=forms.TextInput(attrs={'autofocus': True})
    )
    class Meta:
        model=models.Exam
        fields=['exam_name','questiontpye']

class McqQuestionForm(forms.ModelForm):
    examID=forms.ModelChoiceField(queryset=models.Exam.objects.all().filter(questiontpye='MCQ'),empty_label="Exam Name", to_field_name="id")
    class Meta:
        model=models.McqQuestion
        fields=['marks','question','option1','option2','option3','option4','answer']
        widgets = {
            'question': forms.Textarea(attrs={'rows': 3, 'cols': 50,'autofocus': True})
        }

class ShortQuestionForm(forms.ModelForm):
    examID=forms.ModelChoiceField(queryset=models.Exam.objects.all().filter(questiontpye='ShortAnswer'),empty_label="Exam Name", to_field_name="id")
    class Meta:
        model=models.McqQuestion
        fields=['marks','question']
        widgets = {
            'question': forms.Textarea(attrs={'rows': 3, 'cols': 50, 'autofocus': True})
        }

class PlayListForm(forms.ModelForm):
    class Meta:
        model=models.Playlist
        fields=['name','playlist_id']

class K8STerminalForm(forms.ModelForm):
    learnerID=forms.ModelChoiceField(queryset= User.objects.all().filter(id__in = UserSocialAuth.objects.all().filter(Q(utype=0) | Q(utype=2),status = 1)),empty_label="Learner Name", to_field_name="id")
    
    class Meta:
        model=models.K8STerminal
        fields=['Password','usagevalue']