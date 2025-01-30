from django.db import models
import datetime
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.db.models import Q, Sum
import requests
import humanize
from django.contrib.auth.models import User

class User(AbstractUser):
    user_full_name = models.CharField(max_length=200, null=True, blank=True)
    email = models.CharField(max_length=200, null=True)
    USER_TYPE_CHOICES = (
        ("1", "TRAINER"),
        ("2", "LEARNER"),
        ("3", "CTO"),
        ("4", "CFO"),
        ("5","MENTOR"),
        ("6","STAFF"),
    )
    utype = models.CharField(max_length=200, choices=USER_TYPE_CHOICES, default="2")
    mobile = models.CharField(max_length=10, null=True, blank=True)
    whatsappno = models.CharField(max_length=10, null=True, blank=True)
    profile_pic = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    profile_updated = models.BooleanField(default=False)
    status = models.BooleanField(default=False)
    created =  models.DateTimeField(default=timezone.now)
    
    regdate =  models.DateTimeField(default=datetime.datetime.now)
    skills = models.CharField(default='',max_length=200, null=True, blank=True)
    bio = models.CharField(default='',max_length=2000, null=True, blank=True)
    
    def save(self, *args, **kwargs):
        self.user_full_name = f"{self.first_name.strip()} {self.last_name.strip()}".strip()
        super(User, self).save(*args, **kwargs)
    
class UserLog(models.Model):
    user=models.ForeignKey(User,on_delete=models.SET_NULL, null=True)
    login =  models.DateTimeField(default=datetime.datetime.now)
    logout = models.DateTimeField(default=datetime.datetime.now)
    dur = models.CharField(default='',max_length=200)
    session_id = models.CharField(default='',max_length=200)


class Subject(models.Model):  # Subject
    youtube_id = models.CharField(max_length=100, unique=True, null=True, blank=True)
    subject_name = models.CharField(max_length=200)
    is_active = models.BooleanField(default=True)  # Tracks active/inactive state
    is_youtube = models.BooleanField(default=False)  # True for YouTube Subjects
    last_synced = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.subject_name


class Chapter(models.Model):  # Chapter
    youtube_id = models.CharField(max_length=100, unique=True, null=True, blank=True)
    chapter_name = models.CharField(max_length=200)
    subject = models.ForeignKey(Subject, on_delete=models.SET_NULL, null=True)
    is_active = models.BooleanField(default=True)  # Tracks active/inactive state
    is_youtube = models.BooleanField(default=False)  # True for YouTube Chapters
    last_synced = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.chapter_name

class Topic(models.Model):
    topic_name = models.CharField(max_length=200)
    subject = models.ForeignKey(Subject, on_delete=models.SET_NULL, null=True)
    chapter = models.ForeignKey(Chapter, on_delete=models.SET_NULL, null=True)

    def save(self, *args, **kwargs):
        # Automatically set the subject from the chapter if it's not set
        if not self.subject and self.chapter:
            self.subject = self.chapter.subject
        super().save(*args, **kwargs)
        
    def __str__(self):
        return self.topic_name
        
class Category(models.Model):
    category_name = models.CharField(max_length=200)

    def __str__(self):
        try:
            return self.category_name
        except:
            return self

class SubCategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    subcategory_name = models.CharField(max_length=200)

    def __str__(self):
        return self.subcategory_name
    
class Course(models.Model):
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    subcategory = models.ForeignKey(SubCategory, on_delete=models.SET_NULL, null=True)
    course_name = models.CharField(max_length=200)
    description = models.CharField(max_length=1000,default='')
    whatlearn = models.CharField(max_length=1000,default='')
    includes = models.CharField(max_length=1000,default='')
    cat=(('1','Advanced'),('2','Easy'),('3','Intermideate'))
    themecolor=models.CharField(max_length=200,choices=cat,default='Green')
    tags = models.CharField(max_length=10000,default='')
    image = models.CharField(max_length=1000,default='')
    banner = models.CharField(max_length=1000,default='')
    price = models.IntegerField(default=0)
    
    def __str__(self):
        return self.course_name

class CourseChapter(models.Model):
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True)
    subject = models.ForeignKey(Subject, on_delete=models.SET_NULL, null=True)
    chapter = models.ForeignKey(Chapter, on_delete=models.SET_NULL, null=True)
    def __str__(self):
        return self.chapter.chapter_name





    

class Material(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.SET_NULL, null=True)
    chapter = models.ForeignKey(Chapter, on_delete=models.SET_NULL, null=True)
    id = models.AutoField(primary_key=True)
    serial_number = models.IntegerField(default=0)
    topic = models.CharField(max_length=200)
    cat = (('PDF', 'PDF'), ('HTML', 'HTML'), ('Chapter', 'Chapter'), ('URL', 'URL'))
    mtype = models.CharField(max_length=200, choices=cat, default='PDF')
    urlvalue = models.CharField(max_length=2000)
    description = models.CharField(max_length=200)

    class Meta:
        ordering = ['subject', 'chapter', 'serial_number']

    def save(self, *args, **kwargs):
        if not self.serial_number:
            last_material = Material.objects.filter(
                subject=self.subject,
                chapter=self.chapter
            ).order_by('-serial_number').first()
            if last_material:
                self.serial_number = last_material.serial_number + 1
            else:
                self.serial_number = 1
        super(Material, self).save(*args, **kwargs)



class CourseType(models.Model):
    coursetype_name = models.CharField(max_length=200)

    def __str__(self):
        return self.coursetype_name

class Batch(models.Model):
    batch_name = models.CharField(max_length=50)
    coursetype = models.ForeignKey('CourseType', on_delete=models.SET_NULL, null=True)  # Deletes linked batches if coursetype is deleted
    stdate = models.DateField()
    enddate = models.DateField()

    def __str__(self):
        return self.batch_name


class BatchCourse(models.Model):
    batch = models.ForeignKey(Batch, on_delete=models.SET_NULL, null=True, related_name='batch_courses')  # Tightly linked to Batch
    course = models.ForeignKey('Course', on_delete=models.SET_NULL, null=True)  # Links to a specific course

    def __str__(self):
        return f"{self.batch.batch_name} - {self.course.course_name}"


class BatchTrainer(models.Model):
    batch = models.ForeignKey(Batch, on_delete=models.SET_NULL, null=True, related_name='batch_trainers')  # Tightly linked to Batch
    trainer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)  # Links to a specific trainer

    def __str__(self):
        return f"{self.batch.batch_name} - {self.trainer.username}"


class BatchLearner(models.Model):
    batch = models.ForeignKey(Batch, on_delete=models.SET_NULL, null=True, related_name='batch_learners')  # Tightly linked to Batch
    learner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)  # Links to a specific learner
    fee = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.batch.batch_name} - {self.learner.username}"


class BatchRecordedVDOList(models.Model):
    batch = models.ForeignKey(Batch, on_delete=models.SET_NULL, null=True, related_name='batch_videos')  # Tightly linked to Batch
    subject = models.ForeignKey('Subject', on_delete=models.SET_NULL, null=True)  # Links to a specific subject

    def __str__(self):
        return f"{self.batch.batch_name} - {self.subject.subject_name}"


class Exam(models.Model):
   batch=models.ForeignKey(Batch,on_delete=models.SET_NULL, null=True)
   exam_name = models.CharField(max_length=50)
   cat=(('MCQ','MCQ'),('ShortAnswer','ShortAnswer'))
   questiontpye=models.CharField(max_length=200,choices=cat,default='')
   def __str__(self):
        return self.exam_name

class McqQuestion(models.Model):
   exam=models.ForeignKey(Exam,on_delete=models.SET_NULL, null=True)
   question=models.CharField(max_length=600)
   option1=models.CharField(max_length=200)
   option2=models.CharField(max_length=200)
   option3=models.CharField(max_length=200)
   option4=models.CharField(max_length=200)
   cat=(('1','Option1'),('2','Option2'),('3','Option3'),('4','Option4'))
   answer=models.CharField(max_length=200,choices=cat)
   marks=models.IntegerField(default=0)

class McqResult(models.Model):
    learner=models.ForeignKey(User,on_delete=models.SET_NULL, null=True)
    exam = models.ForeignKey(Exam,on_delete=models.SET_NULL, null=True)
    marks = models.PositiveIntegerField()
    wrong = models.PositiveIntegerField()
    correct = models.PositiveIntegerField()
    timetaken = models.CharField(max_length=200)
    date = models.DateTimeField(auto_now=True)

class McqResultDetails(models.Model):
    mcqresult=models.ForeignKey(McqResult,on_delete=models.SET_NULL, null=True)
    question = models.ForeignKey(McqQuestion,on_delete=models.SET_NULL, null=True)
    selected=models.CharField(max_length=200)

class ShortQuestion(models.Model):
   exam=models.ForeignKey(Exam,on_delete=models.SET_NULL, null=True)
   question=models.CharField(max_length=600)
   marks=models.IntegerField(default=0)

class ShortResult(models.Model):
    learner=models.ForeignKey(User,on_delete=models.SET_NULL, null=True)
    exam = models.ForeignKey(Exam,on_delete=models.SET_NULL, null=True)
    marks = models.PositiveIntegerField()
    datecreate = models.DateTimeField(auto_now=True)
    status= models.BooleanField(default=False)
    timetaken = models.CharField(max_length=200)

class ShortResultDetails(models.Model):
    shortresult=models.ForeignKey(ShortResult,on_delete=models.SET_NULL, null=True)
    question=models.ForeignKey(ShortQuestion,on_delete=models.SET_NULL, null=True)
    marks=models.PositiveIntegerField()
    answer=models.CharField(max_length=200)
    feedback=models.CharField(max_length=200,default='')


class YTExamQuestion(models.Model):
   Subject=models.ForeignKey(Subject,on_delete=models.SET_NULL, null=True)
   Chapter=models.ForeignKey(Chapter,on_delete=models.SET_NULL, null=True)
   question=models.CharField(max_length=600)
   option1=models.CharField(max_length=200)
   option2=models.CharField(max_length=200)
   option3=models.CharField(max_length=200)
   option4=models.CharField(max_length=200)
   cat=(('1','Option1'),('2','Option2'),('3','Option3'),('4','Option4'))
   answer=models.CharField(max_length=200,choices=cat)
   marks=models.IntegerField(default=1)

class YTExamResult(models.Model):
    learner=models.ForeignKey(User,on_delete=models.SET_NULL, null=True)
    ytexamquestion = models.ForeignKey(YTExamQuestion,on_delete=models.SET_NULL, null=True)
    marks = models.PositiveIntegerField()
    wrong = models.PositiveIntegerField()
    correct = models.PositiveIntegerField()
    timetaken = models.CharField(max_length=200)
    date = models.DateTimeField(auto_now=True)

class YTExamResultDetails(models.Model):
    ytexamresult=models.ForeignKey(YTExamResult,on_delete=models.SET_NULL, null=True)
    question = models.ForeignKey(YTExamQuestion,on_delete=models.SET_NULL, null=True)
    selected=models.CharField(max_length=200)

class ChapterToUnlock(models.Model):
    Subject=models.ForeignKey(Subject,on_delete=models.SET_NULL, null=True)
    Chapter=models.ForeignKey(Chapter,on_delete=models.SET_NULL, null=True)
    learner=models.ForeignKey(User,on_delete=models.SET_NULL, null=True)

class ChapterWatched(models.Model):
    Chapter=models.ForeignKey(Chapter,on_delete=models.SET_NULL, null=True)
    learner=models.ForeignKey(User,on_delete=models.SET_NULL, null=True)

class LearnerSubjectCount(models.Model):
    Subject=models.ForeignKey(Subject,on_delete=models.SET_NULL, null=True)
    learner=models.ForeignKey(User,on_delete=models.SET_NULL, null=True)
    count = models.PositiveIntegerField(default=0)

class SessionMaterial(models.Model):
    Subject=models.ForeignKey(Subject,on_delete=models.SET_NULL, null=True)
    Chapter=models.ForeignKey(Chapter,on_delete=models.SET_NULL, null=True)
    cat=(('PDF','PDF'),('HTML','HTML'),('Chapter','Chapter'),('URL','URL'))
    mtype=models.CharField(max_length=200,choices=cat, default= 'PDF')
    urlvalue=models.CharField(max_length=200)
    description=models.CharField(max_length=200)

class LearnerMaterialWatched(models.Model):
    learner=models.ForeignKey(User,on_delete=models.SET_NULL, null=True)
    course=models.ForeignKey(Course,on_delete=models.SET_NULL, null=True)
    chapter=models.ForeignKey(Chapter,on_delete=models.SET_NULL, null=True)
    material=models.ForeignKey(Material,on_delete=models.SET_NULL, null=True)

class LastUserLogin(models.Model):
    user=models.ForeignKey(User,on_delete=models.SET_NULL, null=True)


class ChapterQuestion(models.Model):
   subject=models.ForeignKey(Subject,on_delete=models.SET_NULL, null=True)
   chapter=models.ForeignKey(Chapter,on_delete=models.SET_NULL, null=True)
   question=models.CharField(max_length=600)
   option1=models.CharField(max_length=200)
   option2=models.CharField(max_length=200)
   option3=models.CharField(max_length=200)
   option4=models.CharField(max_length=200)
   cat=(('1','Option1'),('2','Option2'),('3','Option3'),('4','Option4'))
   answer=models.CharField(max_length=200,choices=cat)
   marks=models.IntegerField(default=0)

class ChapterResult(models.Model):
    learner=models.ForeignKey(User,on_delete=models.SET_NULL, null=True)
    course = models.ForeignKey(Course,on_delete=models.SET_NULL, null=True)
    subject = models.ForeignKey(Subject,on_delete=models.SET_NULL, null=True)
    chapter = models.ForeignKey(Chapter,on_delete=models.SET_NULL, null=True)
    marks = models.PositiveIntegerField()
    wrong = models.PositiveIntegerField()
    correct = models.PositiveIntegerField()
    timetaken = models.CharField(max_length=200)
    date = models.DateTimeField(auto_now=True)
    def get_percentage(self):
        try:
            perc = self.correct * 100 / (self.wrong + self.correct)
        except:
            perc = self.correct * 100 / 1
        return perc

class ChapterResultDetails(models.Model):
    chapterresult=models.ForeignKey(ChapterResult,on_delete=models.SET_NULL, null=True)
    question = models.ForeignKey(ChapterQuestion,on_delete=models.SET_NULL, null=True)
    selected=models.CharField(max_length=200)

class UserActivity(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    url = models.CharField(max_length=2048)
    method = models.CharField(max_length=16)
    status_code = models.IntegerField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f'{self.user.username} accessed {self.url} ({self.status_code})'


class ErrorLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    url = models.CharField(max_length=2048)
    exception = models.TextField()
    traceback = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f'Error occurred while processing {self.url}'

class LearnerCart(models.Model):
    learner=models.ForeignKey(User,on_delete=models.SET_NULL, null=True)
    course = models.ForeignKey(Course,on_delete=models.SET_NULL, null=True)
    status=models.IntegerField(default=0)

class K8STerminal(models.Model):
    trainer=models.ForeignKey(User,on_delete=models.SET_NULL, null=True, related_name='%(class)s_requests_trainer')
    learner=models.ForeignKey(User,on_delete=models.SET_NULL, null=True, related_name='%(class)s_requests_learner')
    Password=models.TextField()
    usagevalue=models.PositiveIntegerField(default=0)

class K8STerminalLearnerCount(models.Model):
    learner=models.ForeignKey(User,on_delete=models.SET_NULL, null=True)
    usedvalue=models.PositiveIntegerField(default=0)
    

class Scheduler(models.Model):
    TRAINING_SESSION = '1'
    INTERVIEW = '2'
    CLIENT_REQUIREMENT = '3'
    LAB_CALL = '4'
    MEETING = '5'
    OTHERS = '6'

    SCHEDULER_TYPES = [
        (TRAINING_SESSION, 'Session'),
        (INTERVIEW, 'Interview'),
        (CLIENT_REQUIREMENT, 'Client Requirement'),
        (LAB_CALL, 'Lab Call'),
        (MEETING, 'Meeting'),
        (OTHERS, 'Others'),
    ]

    trainer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    type = models.CharField(max_length=2, choices=SCHEDULER_TYPES, null=True)
    subject = models.ForeignKey(Subject, on_delete=models.SET_NULL, null=True)
    chapter = models.ForeignKey(Chapter, on_delete=models.SET_NULL, null=True)
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True)
    start = models.DateTimeField()
    end = models.DateTimeField(null=True, blank=True)
    eventdetails = models.CharField(max_length=200, null=True)
    meeting_link = models.URLField(max_length=500, null=True, blank=True)

    def __str__(self):
        return f"Schedule on {self.start.strftime('%Y-%m-%d %H:%M:%S')}"

class SchedulerStatus(models.Model): 
    date = models.DateField()
    scheduler=models.ForeignKey(Scheduler,on_delete=models.SET_NULL, null=True)
    trainer=models.ForeignKey(User,on_delete=models.SET_NULL, null=True)
    status=models.PositiveIntegerField(default=0)




class Activity(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.SET_NULL, null=True)
    chapter = models.ForeignKey(Chapter, on_delete=models.SET_NULL, null=True)
    id = models.AutoField(primary_key=True)
    serial_number = models.IntegerField(default=0)
    urlvalue = models.CharField(max_length=2000)
    description = models.CharField(max_length=200)
    class Meta:
        ordering = ['subject', 'chapter', 'serial_number']

    def save(self, *args, **kwargs):
        if not self.serial_number:
            last_material = Activity.objects.filter(
                subject=self.subject,
                chapter=self.chapter
            ).order_by('-serial_number').first()
            if last_material:
                self.serial_number = last_material.serial_number + 1
            else:
                self.serial_number = 1
        super(Activity, self).save(*args, **kwargs)


class ActivityAnswers(models.Model):
    activity = models.ForeignKey(Activity, on_delete=models.SET_NULL, null=True)
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True)
    chapter = models.ForeignKey(Chapter, on_delete=models.SET_NULL, null=True)
    learner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    file_url = models.URLField()
    marks = models.IntegerField(default=0)
    remarks = models.CharField(max_length=2000, default='')
    status = models.BooleanField(default=False)
    submitted_on = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.file_url