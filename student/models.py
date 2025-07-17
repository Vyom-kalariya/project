from django.db import models
from django.contrib.auth.models import User

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student_profile', null=True,blank=True)
    name = models.CharField(max_length=50)
    roll = models.IntegerField()
    enroll = models.CharField(max_length=14)
    photo = models.ImageField(upload_to='student/images')
    url = models.URLField(blank=True)
    email = models.EmailField()
    desc = models.TextField()
    Python = models.IntegerField(default=0)
    FSD = models.IntegerField(default=0)
    TOC = models.IntegerField(default=0)

    def __str__(self):
        return self.name

