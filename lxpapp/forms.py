from django import forms
from social_django.models import UserSocialAuth

from . import models


class ContactusForm(forms.Form):
    Name = forms.CharField(max_length=30)
    Email = forms.EmailField()
    Message = forms.CharField(max_length=500,widget=forms.Textarea(attrs={'rows': 3, 'cols': 30}))

class PassionateSkillForm(forms.ModelForm):
    passionateskill_name = forms.CharField(
        max_length=90000,
        #  forms ↓
        widget=forms.TextInput(attrs={'autofocus': True})
    )
    class Meta:
        model=models.PassionateSkill
        fields=['passionateskill_name']

class KnownSkillForm(forms.ModelForm):
    knownskill_name = forms.CharField(
        max_length=90000,
        #  forms ↓
        widget=forms.TextInput(attrs={'autofocus': True})
    )
    class Meta:
        model=models.KnownSkill
        fields=['knownskill_name']

class SubjectForm(forms.ModelForm):
    subject_name = forms.CharField(
        max_length=90000,
        #  forms ↓
        widget=forms.TextInput(attrs={'autofocus': True})
    )
    class Meta:
        model=models.Subject
        fields=['subject_name']

class ModuleForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ModuleForm, self).__init__(*args, **kwargs)
    
    class Meta:
        model=models.Module
        fields=['module_name','subject']

class ChapterForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ChapterForm, self).__init__(*args, **kwargs)
    class Meta:
        model=models.Chapter
        fields=['chapter_name','module']

class TopicForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(TopicForm, self).__init__(*args, **kwargs)
    class Meta:
        model=models.Topic
        fields=['topic_name','chapter']

class LearnerDetailsForm(forms.ModelForm):
    user_full_name = forms.CharField(
        max_length=90000,
        #  forms ↓
        widget=forms.TextInput(attrs={'autofocus': True})
    )
    class Meta:
        model=models.LearnerDetails
        fields=['user_full_name','mobile','iswhatsapp','whatsappno']

class CourseForm(forms.ModelForm):
    class Meta:
        model = models.Course
        fields = ('course_name', 'subject', 'module', 'chapter', 'topic')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class CourseSetForm(forms.ModelForm):
    class Meta:
        model = models.CourseSet
        fields = ('courseset_name', 'subject', 'module', 'chapter', 'topic')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class TrainerNotificationForm(forms.ModelForm):
    trainerID=forms.ModelChoiceField(queryset=UserSocialAuth.objects.all().filter(utype = '1',user_id__in=models.User.objects.all().order_by('first_name')),empty_label="Trainer Name", to_field_name="id")
    trainernotification_message = forms.CharField(
        max_length=255,
        #  forms ↓
        widget=forms.TextInput(attrs={'autofocus': True})
    )
    class Meta:
        model=models.TrainerNotification
        fields=['trainernotification_message']        

class MaterialForm(forms.ModelForm):
    class Meta:
        model = models.Material
        fields = ('subject', 'module', 'chapter', 'topic','mtype','urlvalue','description')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['module'].queryset = models.Module.objects.none()

        if 'subject' in self.data:
            try:
                subject_id = int(self.data.get('subject'))
                self.fields['module'].queryset = models.Module.objects.filter(subject_id=subject_id).order_by('module_name')
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            self.fields['module'].queryset = self.instance.subject.module_set.order_by('subject_name')

        self.fields['chapter'].queryset = models.Module.objects.none()
        if 'module' in self.data:
            try:
                module_id = int(self.data.get('module'))
                self.fields['chapter'].queryset = models.Chapter.objects.filter(module_id=module_id).order_by('chapter_name')
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            self.fields['chapter'].queryset = self.instance.module.chapter_set.order_by('chapter_name')


        self.fields['topic'].queryset = models.Chapter.objects.none()
        if 'chapter' in self.data:
            try:
                chapter_id = int(self.data.get('chapter'))
                self.fields['topic'].queryset = models.Topic.objects.filter(chapter_id=chapter_id).order_by('topic_name')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty Topic queryset
        elif self.instance.pk:
            self.fields['topic'].queryset = self.instance.chapter.topic_set.order_by('topic_name')

class CourseTypeForm(forms.ModelForm):
    coursetype_name = forms.CharField(
        max_length=90000,
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
