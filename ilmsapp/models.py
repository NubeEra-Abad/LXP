from django.db import models
from django.urls import reverse
from social_django import models as UMODEL
from django.contrib.auth.models import User
class Subject(models.Model):
   subject_name = models.CharField(max_length=50)
   playlist_id = models.CharField(max_length=50)
   def __str__(self):
      return self.subject_name

class Chapter(models.Model):
   subject=models.ForeignKey(Subject,on_delete=models.CASCADE)
   chapter_name = models.CharField(max_length=50)
   def __str__(self):
      return self.chapter_name

class Topic(models.Model):
   chapter=models.ForeignKey(Chapter,on_delete=models.CASCADE)
   subject=models.ForeignKey(Subject,on_delete=models.CASCADE)
   topic_name = models.CharField(max_length=50)
   def __str__(self):
      return self.topic_name
class Course(models.Model):
   course_name = models.CharField(max_length=50)
   
   def get_absolute_url(self):
        return reverse('course-update', kwargs={'pk': self.pk})

   def __str__(self):
        return f"{self.course_name}"

class CourseDetails(models.Model):
   course=models.ForeignKey(Course,on_delete=models.CASCADE)
   subject=models.ForeignKey(Subject,on_delete=models.CASCADE)
   chapter=models.ForeignKey(Chapter,on_delete=models.CASCADE)
   topic=models.ForeignKey(Topic,on_delete=models.CASCADE)

class UserCourse(models.Model):
   user = models.ForeignKey(User,on_delete=models.CASCADE)
   course=models.ForeignKey(Course,on_delete=models.CASCADE)
   remarks = models.CharField(max_length=50)

class CourseType(models.Model):
   coursetype_name = models.CharField(max_length=50)
   def __str__(self):
      return self.coursetype_name

class Batch(models.Model):
   batch_name = models.CharField(max_length=50)
   course=models.ForeignKey(Course,on_delete=models.CASCADE)
   coursetype=models.ForeignKey(CourseType,on_delete=models.CASCADE)
   stdate = models.DateField()
   enddate = models.DateField()
   def __str__(self):
      return self.batch_name

class BatchTrainer(models.Model):
   batch=models.ForeignKey(Batch,on_delete=models.CASCADE)
   trainer=models.ForeignKey(UMODEL.UserSocialAuth,on_delete=models.CASCADE)

class PassionateSkill(models.Model):
   passionateskill_name = models.CharField(max_length=200)
   def __str__(self):
        return self.passionateskill_name

class KnownSkill(models.Model):
   knownskill_name = models.CharField(max_length=200)
   def __str__(self):
        return self.knownskill_name

class LearnerDetails(models.Model):
    learner=models.ForeignKey(User,on_delete=models.CASCADE)
    user_full_name = models.CharField(max_length=200)
    mobile = models.IntegerField(default=0)
    iswhatsapp = models.BooleanField(default=False)
    whatsappno = models.IntegerField(default=0)
    
class LearnerDetailsPSkill(models.Model):
    learnerdetails=models.ForeignKey(LearnerDetails,on_delete=models.CASCADE)
    passionateskill=models.ForeignKey(PassionateSkill,on_delete=models.CASCADE)

class LearnerDetailsKSkill(models.Model):
    learnerdetails=models.ForeignKey(LearnerDetails,on_delete=models.CASCADE)
    knownskill=models.ForeignKey(KnownSkill,on_delete=models.CASCADE)

class IsFirstLogIn(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    def __str__(self):
        return self.user


class Exam(models.Model):
   exam_name = models.CharField(max_length=50)
   course=models.ForeignKey(Course,on_delete=models.CASCADE)
   cat=(('MCQ','MCQ'),('ShortAnswer','ShortAnswer'))
   questiontpye=models.CharField(max_length=200,choices=cat,default='')
   def __str__(self):
        return self.exam_name

class McqQuestion(models.Model):
   exam=models.ForeignKey(Exam,on_delete=models.CASCADE)
   question=models.CharField(max_length=600)
   option1=models.CharField(max_length=200)
   option2=models.CharField(max_length=200)
   option3=models.CharField(max_length=200)
   option4=models.CharField(max_length=200)
   cat=(('1','Option1'),('2','Option2'),('3','Option3'),('4','Option4'))
   answer=models.CharField(max_length=200,choices=cat)
   marks=models.IntegerField(default=0)

class ShortQuestion(models.Model):
   exam=models.ForeignKey(Exam,on_delete=models.CASCADE)
   question=models.CharField(max_length=600)
   marks=models.IntegerField(default=0)

class PlayList(models.Model):
   playlist_name = models.CharField(max_length=200)
   playlist_id = models.CharField(max_length=200)
   def __str__(self):
        return self.playlist_name
   
class VideoLinks(models.Model):
   subject=models.ForeignKey(Subject,on_delete=models.CASCADE)
   chapter=models.ForeignKey(Chapter,on_delete=models.CASCADE)
   SrNo=models.PositiveIntegerField()
   Url=models.CharField(max_length=200)
   video_id=models.CharField(max_length=200)
   TopicCovered=models.PositiveIntegerField(default=0)