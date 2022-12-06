from django.db import models
from django.urls import reverse
from social_django import models as UMODEL
class Subject(models.Model):
   subject_name = models.CharField(max_length=50)
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
   course=models.ForeignKey(Course,on_delete=models.CASCADE)
   remarks = models.CharField(max_length=50)
   user_id = models.IntegerField(default=0)

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
   