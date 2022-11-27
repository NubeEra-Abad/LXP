from django.db import models
from django.contrib.auth.models import User

class Learner(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE) 
    address = models.CharField(max_length=40)
    mobile = models.CharField(max_length=20,null=False)
    status= models.BooleanField(default=False)

    @property
    def get_name(self):
        return self.user.first_name
    @property
    def get_course(self):
        return self.user.last_name
    @property
    def get_instance(self):
        return self
    def __str__(self):
        return self.user.first_name