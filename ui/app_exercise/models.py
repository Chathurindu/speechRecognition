from django.db import models

# Create your models here.
from app_profile.models import DoctorProfile


class Exercise(models.Model):
    exercise_type = models.CharField(choices=(("video","video"),
                                              ("photo","photo"),
                                              ("physical","physical"),
                                              ("not_define","not_define")),
                                     max_length=20,
                                     default="not_define")
    name = models.CharField(max_length=100,null=True,blank=True)
    category = models.CharField(max_length=100, null=True, blank=True)
    emotion = models.CharField(max_length=100,null=True,blank=True)
    intonations = models.CharField(max_length=100,null=True,blank=True)
    phoneme  = models.CharField(max_length=100,null=True,blank=True)
    doctor = models.ForeignKey(DoctorProfile,on_delete=models.CASCADE)
    file = models.FileField(null=True,blank=True)
    target_age = models.IntegerField(null=True,blank=True)
    description = models.CharField(max_length=1000,null=True,blank=True)

    @property
    def file_uri(self):
        return "/media/" + self.file.__str__()
